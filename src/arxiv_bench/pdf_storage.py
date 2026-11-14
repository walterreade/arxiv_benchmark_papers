"""Ephemeral NVMe PDF staging, local text extraction, and date-sharded GCS archival."""

from __future__ import annotations

import hashlib
import re
import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pymupdf
import pypdf
import requests
import zstandard as zstd
from requests.adapters import HTTPAdapter

from arxiv_bench.config import (
    Settings,
    canonicalize_arxiv_id,
    format_yymm_prefix,
    sanitize_arxiv_id,
)

_REFS_HEADING_RE = re.compile(
    r"^\s*(?:\d+\.?\s+)?(?:references|bibliography)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


class StagingQuotaError(RuntimeError):
    """Raised when ephemeral NVMe PDF staging reaches its configured disk cap."""


class WithdrawnPaperError(RuntimeError):
    """Raised when arXiv returns an HTML withdrawal notice or permanent 404/410."""


@dataclass
class StagedPdf:
    """Temporarily staged local PDF binary on NVMe."""

    arxiv_id: str
    local_path: Path
    source: str
    already_archived_uri: str | None = None
    size_bytes: int = 0


@dataclass(frozen=True)
class ExtractedText:
    """Locally extracted PDF text + diagnostics."""

    plain_text: str
    trimmed_text: str
    compressed_zst: bytes
    page_count: int
    chars_per_page: float


@dataclass(frozen=True)
class ArchiveResult:
    """Outcome of GCS archival and local temp deletion."""

    gcs_pdf_uri: str | None
    pdf_sha256: str
    pdf_sync_status: str
    error_detail: str | None = None


def strip_bibliography(full_text: str) -> str:
    """Trim trailing References/Bibliography section to keep Stage 3 rubric inputs clean."""
    if not full_text:
        return ""
    # Only strip a References heading occurring in the final 45% of the document
    cutoff_start = int(len(full_text) * 0.55)
    matches = list(_REFS_HEADING_RE.finditer(full_text, pos=cutoff_start))
    if not matches:
        return full_text
    return full_text[: matches[-1].start()].rstrip()


def compress_text(text: str) -> bytes:
    """Compress UTF-8 text with zstandard."""
    return zstd.ZstdCompressor(level=6).compress(text.encode("utf-8"))


def decompress_text(blob: bytes | None) -> str:
    """Decompress zstandard UTF-8 text stored in papers.compressed_text_zst."""
    if not blob:
        return ""
    return zstd.ZstdDecompressor().decompress(blob).decode("utf-8", errors="replace")


def extract_local_text(pdf_path: Path) -> ExtractedText:
    """Extract PDF text using PyMuPDF (primary) with pypdf fallback."""
    pages: list[str] = []
    try:
        with pymupdf.open(str(pdf_path)) as doc:
            for page in doc:
                pages.append(page.get_text("text") or "")
    except Exception:  # noqa: BLE001
        reader = pypdf.PdfReader(str(pdf_path))
        for page in reader.pages:
            pages.append(page.extract_text() or "")

    page_count = len(pages)
    full_text = "\n\n".join(pages)
    trimmed = strip_bibliography(full_text)
    chars_per_page = round(len(full_text) / page_count, 2) if page_count > 0 else 0.0
    return ExtractedText(
        plain_text=full_text,
        trimmed_text=trimmed,
        compressed_zst=compress_text(trimmed),
        page_count=page_count,
        chars_per_page=chars_per_page,
    )


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class PdfStorageManager:
    """Manages bounded NVMe PDF staging, tiered cloud sourcing, GCS archival, and cleanup."""

    def __init__(
        self,
        settings: Settings,
        *,
        gcs_client: Any | None = None,
        http_session: requests.Session | None = None,
        export_delay_seconds: float = 3.0,
    ) -> None:
        self._settings = settings
        self._gcs_client = gcs_client
        self._gcs_lock = threading.Lock()
        if http_session is not None:
            self._http = http_session
        else:
            sess = requests.Session()
            adapter = HTTPAdapter(pool_connections=32, pool_maxsize=32)
            sess.mount("https://", adapter)
            sess.mount("http://", adapter)
            self._http = sess
        self._export_delay = export_delay_seconds
        self._export_lock = threading.Lock()
        self._last_export_ts = 0.0

    def _get_gcs(self) -> Any:
        if self._gcs_client is None:
            with self._gcs_lock:
                if self._gcs_client is None:
                    from google.cloud import storage

                    self._gcs_client = storage.Client(
                        project=self._settings.gcp_requester_pays_project
                    )
        return self._gcs_client

    def staged_bytes(self) -> int:
        if not self._settings.staging_dir.exists():
            return 0
        return sum(p.stat().st_size for p in self._settings.staging_dir.rglob("*") if p.is_file())

    def enforce_staging_budget(self) -> None:
        max_bytes = int(self._settings.max_staging_gb * (1024**3))
        current = self.staged_bytes()
        if current >= max_bytes:
            raise StagingQuotaError(
                f"Ephemeral staging directory '{self._settings.staging_dir}' reached "
                f"{current / (1024**3):.2f} GB >= cap {self._settings.max_staging_gb:.2f} GB."
            )

    def stage_pdf(
        self,
        arxiv_id: str,
        *,
        gcs_pdf_uri: str | None = None,
        version: int | None = None,
    ) -> StagedPdf:
        """Download a single PDF into ephemeral NVMe staging in strict priority order."""
        self.enforce_staging_budget()
        self._settings.staging_dir.mkdir(parents=True, exist_ok=True)

        canonical, parsed_ver = canonicalize_arxiv_id(arxiv_id)
        ver = version or parsed_ver
        safe = sanitize_arxiv_id(canonical)
        local_path = self._settings.staging_dir / f"{safe}.pdf"

        # Tier 1: Existing private archive URI in gs://inversion/pdf/...
        if gcs_pdf_uri and gcs_pdf_uri.startswith("gs://"):
            if self._download_gcs_uri(gcs_pdf_uri, local_path, requester_pays=False):
                return StagedPdf(
                    arxiv_id=canonical,
                    local_path=local_path,
                    source="gcs_archive",
                    already_archived_uri=gcs_pdf_uri,
                    size_bytes=local_path.stat().st_size,
                )

        # Tier 2: Cloud-internal transfer from gs://arxiv-dataset/arxiv/...
        if self._download_from_arxiv_gcs(canonical, local_path, version=ver):
            return StagedPdf(
                arxiv_id=canonical,
                local_path=local_path,
                source="gcs_arxiv_dataset",
                already_archived_uri=None,
                size_bytes=local_path.stat().st_size,
            )

        # Tier 3: Rate-limited fallback to https://export.arxiv.org/pdf/<id>
        self._download_from_export_arxiv(canonical, local_path)
        return StagedPdf(
            arxiv_id=canonical,
            local_path=local_path,
            source="export_arxiv",
            already_archived_uri=None,
            size_bytes=local_path.stat().st_size,
        )

    def _download_gcs_uri(
        self,
        uri: str,
        destination: Path,
        *,
        requester_pays: bool,
    ) -> bool:
        stripped = uri[len("gs://") :]
        bucket_name, _, blob_name = stripped.partition("/")
        if not bucket_name or not blob_name:
            return False
        try:
            client = self._get_gcs()
            bucket = (
                client.bucket(bucket_name, user_project=self._settings.gcp_requester_pays_project)
                if requester_pays
                else client.bucket(bucket_name)
            )
            blob = bucket.blob(blob_name)
            if not blob.exists():
                return False
            blob.download_to_filename(str(destination))
            return destination.exists() and destination.stat().st_size > 1000
        except Exception:  # noqa: BLE001
            destination.unlink(missing_ok=True)
            return False

    def _download_from_arxiv_gcs(
        self,
        canonical_id: str,
        destination: Path,
        *,
        version: int | None = None,
    ) -> bool:
        yymm = format_yymm_prefix(canonical_id)
        if "/" in canonical_id:
            archive, num = canonical_id.split("/", 1)
            prefix = f"arxiv/{archive}/pdf/{yymm}/{num}"
        else:
            prefix = f"arxiv/arxiv/pdf/{yymm}/{canonical_id}"

        candidates = (
            [f"{prefix}v{version}.pdf", f"{prefix}v1.pdf"]
            if version
            else [f"{prefix}v1.pdf", f"{prefix}v2.pdf", f"{prefix}.pdf"]
        )
        for blob_path in candidates:
            uri = f"gs://{self._settings.gcs_arxiv_bucket}/{blob_path}"
            if self._download_gcs_uri(uri, destination, requester_pays=True):
                return True
        return False

    def _download_from_export_arxiv(self, canonical_id: str, destination: Path) -> None:
        with self._export_lock:
            elapsed = time.monotonic() - self._last_export_ts
            if self._export_delay > 0 and elapsed < self._export_delay:
                time.sleep(self._export_delay - elapsed)
            self._last_export_ts = time.monotonic()

        urls = (
            f"https://export.arxiv.org/pdf/{canonical_id}.pdf",
            f"https://arxiv.org/pdf/{canonical_id}",
        )
        last_exc: Exception | None = None
        resp: requests.Response | None = None
        for idx, url in enumerate(urls):
            try:
                cand = self._http.get(
                    url,
                    headers={"User-Agent": "arxiv-bench/0.2 (personal AI benchmark research)"},
                    timeout=60,
                )
                if cand.status_code in (403, 404, 410):
                    raise WithdrawnPaperError(f"HTTP {cand.status_code} for {canonical_id}")
                cand.raise_for_status()
                resp = cand
                break
            except WithdrawnPaperError:
                raise
            except requests.RequestException as exc:
                last_exc = exc
                if idx + 1 < len(urls):
                    time.sleep(1.0)
                    continue
                raise
        assert resp is not None or last_exc is not None
        if resp is None:
            raise last_exc  # type: ignore[misc]

        content_type = resp.headers.get("Content-Type", "").lower()
        if "text/html" in content_type or len(resp.content) < 1000:
            raise WithdrawnPaperError(
                f"Withdrawn or invalid PDF response for {canonical_id} "
                f"(content-type={content_type}, bytes={len(resp.content)})"
            )
        destination.write_bytes(resp.content)

    def archive_and_cleanup(
        self,
        staged: StagedPdf,
        *,
        published_date: str | None = None,
    ) -> ArchiveResult:
        """Archive newly fetched PDF to gs://inversion/pdf/<YYMM>/<safe_id>.pdf and delete local copy."""
        pdf_sha = ""
        try:
            pdf_sha = _sha256_file(staged.local_path)
            if staged.already_archived_uri:
                return ArchiveResult(
                    gcs_pdf_uri=staged.already_archived_uri,
                    pdf_sha256=pdf_sha,
                    pdf_sync_status="synced",
                )

            yymm = format_yymm_prefix(staged.arxiv_id, published_date)
            safe = sanitize_arxiv_id(staged.arxiv_id)
            blob_name = f"pdf/{yymm}/{safe}.pdf"
            target_uri = f"gs://{self._settings.gcs_archive_bucket}/{blob_name}"

            try:
                client = self._get_gcs()
                bucket = client.bucket(self._settings.gcs_archive_bucket)
                blob = bucket.blob(blob_name)
                blob.upload_from_filename(str(staged.local_path), content_type="application/pdf")
                if not blob.exists():
                    return ArchiveResult(
                        gcs_pdf_uri=None,
                        pdf_sha256=pdf_sha,
                        pdf_sync_status="pending_upload",
                        error_detail="GCS existence verification failed after upload",
                    )
                return ArchiveResult(
                    gcs_pdf_uri=target_uri,
                    pdf_sha256=pdf_sha,
                    pdf_sync_status="synced",
                )
            except Exception as exc:  # noqa: BLE001
                return ArchiveResult(
                    gcs_pdf_uri=None,
                    pdf_sha256=pdf_sha,
                    pdf_sync_status="pending_upload",
                    error_detail=str(exc)[:500],
                )
        finally:
            staged.local_path.unlink(missing_ok=True)

    def cleanup_staged(self, staged: StagedPdf) -> None:
        """Unconditionally remove a temporary staged PDF from NVMe."""
        staged.local_path.unlink(missing_ok=True)

    def index_existing_gcs_pdfs(self, conn: sqlite3.Connection, *, prefix: str = "pdf/") -> int:
        """Index existing gs://inversion/pdf/ objects into papers.gcs_pdf_uri without moving them."""
        client = self._get_gcs()
        blobs = client.list_blobs(self._settings.gcs_archive_bucket, prefix=prefix)
        updated = 0
        batch: list[tuple[str, str]] = []

        for blob in blobs:
            name = str(blob.name)
            if not name.lower().endswith(".pdf"):
                continue
            rel = name[len(prefix) :] if name.startswith(prefix) else name
            parts = rel.split("/")
            if len(parts) == 2 and not parts[0].isdigit():
                # Legacy category subdirectory e.g. pdf/cs/0311046.pdf
                raw_id = f"{parts[0]}/{parts[1]}"
            else:
                raw_id = parts[-1]
            canonical, _ = canonicalize_arxiv_id(raw_id)
            uri = f"gs://{self._settings.gcs_archive_bucket}/{name}"
            batch.append((uri, canonical))
            if len(batch) >= 500:
                updated += self._apply_gcs_uri_batch(conn, batch)
                batch.clear()

        if batch:
            updated += self._apply_gcs_uri_batch(conn, batch)
        return updated

    @staticmethod
    def _apply_gcs_uri_batch(conn: sqlite3.Connection, batch: list[tuple[str, str]]) -> int:
        cur = conn.cursor()
        cur.executemany(
            """
            UPDATE papers
            SET gcs_pdf_uri = COALESCE(gcs_pdf_uri, ?),
                pdf_sync_status = 'synced'
            WHERE arxiv_id = ?
            """,
            batch,
        )
        conn.commit()
        return cur.rowcount
