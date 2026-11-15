"""Centralized settings and canonical arXiv ID helpers."""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_LEGACY_ROOT = Path("/mnt/filestore/walter/lds_projects/arxiv_benchmark_papers")
DEFAULT_DB_PATH = Path.home() / ".local" / "share" / "arxiv_bench" / "benchmarks.db"
DEFAULT_STAGING_DIR = Path.home() / ".cache" / "arxiv_bench" / "staging"
DEFAULT_LOG_DIR = Path.home() / ".local" / "state" / "arxiv_bench" / "logs"
DEFAULT_NFS_BACKUP_DIR = DEFAULT_LEGACY_ROOT / "backups"
ISO_DATE_GLOB = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"

_VERSION_RE = re.compile(r"v(\d+)$", re.IGNORECASE)
_ISO_DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:$|T|\s)")
_MODERN_ID_RE = re.compile(r"^(\d{2})(\d{2})\.\d{4,5}$")
_LEGACY_SLASH_RE = re.compile(r"^([a-z\-]+(?:\.[a-z\-]+)?)/(\d{2})(\d{2})\d{3}$", re.IGNORECASE)
_LEGACY_UNDERSCORE_RE = re.compile(
    r"^([a-z\-]+(?:\.[a-z\-]+)?)_(\d{7})$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Settings:
    """Runtime configuration resolved from environment variables and .env."""

    repo_root: Path
    db_path: Path
    staging_dir: Path
    log_dir: Path
    max_staging_gb: float
    google_api_key: str
    s2_api_key: str
    gcs_archive_bucket: str
    gcs_arxiv_bucket: str
    gcp_requester_pays_project: str
    nfs_backup_dir: Path
    decision_model: str
    flash_model: str
    religion_model: str
    triage_rubric_path: Path

    @classmethod
    def load(cls, env_file: Path | None = None, repo_root: Path | None = None) -> Settings:
        """Load configuration from .env and environment variables."""
        resolved_repo = (repo_root or Path.cwd()).resolve()
        candidate_env = env_file or (resolved_repo / ".env")
        if candidate_env.exists():
            load_dotenv(candidate_env, override=False)

        db_path = Path(os.environ.get("ARXIV_BENCH_DB_PATH", str(DEFAULT_DB_PATH))).expanduser()
        staging_dir = Path(
            os.environ.get("ARXIV_BENCH_STAGING_DIR", str(DEFAULT_STAGING_DIR))
        ).expanduser()
        log_dir = Path(os.environ.get("ARXIV_BENCH_LOG_DIR", str(DEFAULT_LOG_DIR))).expanduser()
        nfs_backup_dir = Path(
            os.environ.get("ARXIV_BENCH_NFS_BACKUP_DIR", str(DEFAULT_NFS_BACKUP_DIR))
        ).expanduser()
        triage_rubric_path = Path(
            os.environ.get(
                "ARXIV_BENCH_TRIAGE_RUBRIC",
                str(resolved_repo / "rubrics" / "stage1_triage_v2.yaml"),
            )
        ).expanduser()

        return cls(
            repo_root=resolved_repo,
            db_path=db_path,
            staging_dir=staging_dir,
            log_dir=log_dir,
            max_staging_gb=float(os.environ.get("ARXIV_BENCH_MAX_STAGING_GB", "10.0")),
            google_api_key=os.environ.get("GOOGLE_API_KEY", ""),
            s2_api_key=os.environ.get("S2_API_KEY", ""),
            gcs_archive_bucket=os.environ.get("GCS_ARCHIVE_BUCKET", "inversion"),
            gcs_arxiv_bucket=os.environ.get("GCS_ARXIV_BUCKET", "arxiv-dataset"),
            gcp_requester_pays_project=os.environ.get(
                "GCP_REQUESTER_PAYS_PROJECT",
                os.environ.get("GOOGLE_CLOUD_PROJECT", "kaggle-comps-162117"),
            ),
            nfs_backup_dir=nfs_backup_dir,
            decision_model=os.environ.get("ARXIV_BENCH_DECISION_MODEL", "models/gemini-decision-1"),
            flash_model=os.environ.get("ARXIV_BENCH_FLASH_MODEL", "gemini-3.8-flash"),
            religion_model=os.environ.get("ARXIV_BENCH_RELIGION_MODEL", "gemini-3.8-flash"),
            triage_rubric_path=triage_rubric_path,
        )


def canonicalize_arxiv_id(raw_id: str) -> tuple[str, int | None]:
    """Normalize an arXiv ID or filename into (canonical_unversioned_id, version_num).

    Handles:
    - '2601.15755v2' -> ('2601.15755', 2)
    - '2601.15755.pdf' -> ('2601.15755', None)
    - 'cs_0311046.json' -> ('cs/0311046', None)
    - 'http://arxiv.org/abs/2501.01234v1' -> ('2501.01234', 1)
    """
    cleaned = raw_id.strip()
    if "arxiv.org/" in cleaned:
        cleaned = re.sub(r"^https?://(?:export\.)?arxiv\.org/(?:abs|pdf)/", "", cleaned).rstrip("/")
    for ext in (".pdf", ".json"):
        if cleaned.lower().endswith(ext):
            cleaned = cleaned[: -len(ext)]

    # Strip leading directory prefix if given a file path unless it's an old-style category/id
    if "/" in cleaned and not _LEGACY_SLASH_RE.match(cleaned.split("v")[0]):
        parts = cleaned.split("/")
        if len(parts) >= 2 and re.match(r"^\d{7}(?:v\d+)?$", parts[-1]):
            cleaned = f"{parts[-2]}/{parts[-1]}"
        else:
            cleaned = parts[-1]

    version: int | None = None
    m_ver = _VERSION_RE.search(cleaned)
    if m_ver:
        version = int(m_ver.group(1))
        cleaned = cleaned[: m_ver.start()]

    m_old = _LEGACY_UNDERSCORE_RE.match(cleaned)
    if m_old:
        cleaned = f"{m_old.group(1)}/{m_old.group(2)}"

    return cleaned, version


def sanitize_arxiv_id(arxiv_id: str) -> str:
    """Convert canonical arXiv ID to filesystem/GCS-safe filename stem."""
    canonical, _ = canonicalize_arxiv_id(arxiv_id)
    return canonical.replace("/", "_")


def unsanitize_arxiv_id(safe_id: str) -> str:
    """Restore canonical arXiv ID from sanitized filename or stem."""
    canonical, _ = canonicalize_arxiv_id(safe_id)
    return canonical


def get_arxiv_url(arxiv_id: str) -> str:
    """Return canonical https://arxiv.org/abs/<id> URL."""
    canonical, _ = canonicalize_arxiv_id(arxiv_id)
    return f"https://arxiv.org/abs/{canonical}"


def compute_metadata_sha256(
    title: str | None,
    abstract: str | None,
    categories: list[str] | str | None,
) -> str:
    """Compute stable SHA-256 over normalized title, abstract, and sorted categories."""
    if isinstance(categories, list):
        cat_str = " ".join(sorted(c.strip() for c in categories if c.strip()))
    else:
        cat_str = " ".join(sorted((categories or "").split()))
    payload = "\n".join(
        [
            " ".join((title or "").split()),
            " ".join((abstract or "").split()),
            cat_str,
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def format_yymm_prefix(arxiv_id: str, published_date: str | None = None) -> str:
    """Compute YYMM date shard prefix for gs://inversion/pdf/<YYMM>/<safe_id>.pdf."""
    canonical, _ = canonicalize_arxiv_id(arxiv_id)
    m_mod = _MODERN_ID_RE.match(canonical)
    if m_mod:
        return f"{m_mod.group(1)}{m_mod.group(2)}"
    m_leg = _LEGACY_SLASH_RE.match(canonical)
    if m_leg:
        return f"{m_leg.group(2)}{m_leg.group(3)}"
    if published_date and len(published_date) >= 7:
        digits = re.sub(r"[^0-9]", "", published_date)
        if len(digits) >= 6:
            return digits[2:6]
    return "0000"


def normalize_published_date(
    raw_date: str | None,
    *,
    arxiv_id: str | None = None,
    fallback_to_id: bool = False,
) -> str | None:
    """Validate and normalize a published date to strict ISO YYYY-MM-DD, or None.

    Rejects placeholder strings such as 'N/A', 'Unknown', 'null', 'XXXX-XX-XX',
    '2022-XX-XX', or invalid calendar dates. When ``fallback_to_id`` is True and
    ``raw_date`` is invalid/missing, derives 'YYYY-MM-01' from the canonical arXiv ID.
    """
    if isinstance(raw_date, str):
        cleaned = raw_date.strip()
        m_iso = _ISO_DATE_PREFIX_RE.match(cleaned)
        if m_iso:
            candidate = m_iso.group(1)
            try:
                datetime.strptime(candidate, "%Y-%m-%d")
                return candidate
            except ValueError:
                pass

    if fallback_to_id and arxiv_id:
        canonical, _ = canonicalize_arxiv_id(arxiv_id)
        m_mod = _MODERN_ID_RE.match(canonical)
        if m_mod:
            yy, mm = int(m_mod.group(1)), int(m_mod.group(2))
            if 1 <= mm <= 12:
                return f"20{yy:02d}-{mm:02d}-01"
        m_leg = _LEGACY_SLASH_RE.match(canonical)
        if m_leg:
            yy, mm = int(m_leg.group(2)), int(m_leg.group(3))
            if 1 <= mm <= 12:
                century = 19 if yy >= 90 else 20
                return f"{century}{yy:02d}-{mm:02d}-01"

    return None
