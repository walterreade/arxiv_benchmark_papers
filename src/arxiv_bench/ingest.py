"""arXiv weekly snapshot sync, category-scoped Atom delta ingestion, and Stage 0 pre-filter."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import requests

from arxiv_bench.config import (
    Settings,
    canonicalize_arxiv_id,
    compute_metadata_sha256,
)
from arxiv_bench.db import SingleWriterQueue

CORE_AI_CATEGORIES = frozenset(
    {
        "cs.AI",
        "cs.CL",
        "cs.CV",
        "cs.LG",
        "cs.MA",
        "cs.RO",
        "cs.SD",
        "cs.IR",
        "cs.HC",
        "cs.CY",
        "cs.NE",
        "cs.SE",
        "cs.CR",
        "stat.ML",
        "eess.AS",
        "eess.IV",
        "eess.SP",
    }
)

RESCUE_CATEGORY_PREFIXES = (
    "q-bio.",
    "physics.",
    "cond-mat.",
    "astro-ph.",
    "econ.",
    "q-fin.",
    "stat.",
    "math.",
    "nlin.",
    "cs.",
)

_AI_TERM_RE = re.compile(
    r"\b("
    r"llm|llms|large language model|language model|foundation model|vision[- ]language|"
    r"multimodal|machine learning|deep learning|neural network|transformer|diffusion model|"
    r"reinforcement learning|artificial intelligence|autonomous agent|ai agent|"
    r"speech recognition|computer vision|generative ai|genai|vlm|vlms|mllm"
    r")\b",
    re.IGNORECASE,
)

_BENCH_TERM_RE = re.compile(
    r"\b("
    r"benchmark|benchmarks|benchmarking|evaluation dataset|evaluation suite|"
    r"evaluation framework|evaluation metric|evaluation methodology|leaderboard|"
    r"testbed|corpus|dataset|bias evaluation|red[- ]teaming|contamination|audit"
    r")\b",
    re.IGNORECASE,
)

DEFAULT_ATOM_QUERIES = (
    "cat:cs.* OR cat:stat.ML OR cat:eess.AS OR cat:eess.IV OR cat:eess.SP",
    '(cat:q-bio.* OR cat:physics.* OR cat:econ.* OR cat:q-fin.*) AND (all:benchmark OR all:dataset) AND (all:"machine learning" OR all:"language model" OR all:"deep learning")',
)

ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}


@dataclass
class SyncStats:
    """Summary counts returned by snapshot or Atom delta ingestion."""

    source: str
    records_read: int = 0
    records_upserted: int = 0
    prefilter_passed: int = 0
    version_drifts: int = 0
    malformed_lines: int = 0
    watermark_date: str | None = None
    incomplete_pagination: bool = False


def passes_stage0_prefilter(
    categories: list[str] | str | None,
    title: str | None,
    abstract: str | None,
) -> bool:
    """$0 deterministic CPU filter passing 100% of AI categories + non-CS AI benchmark rescues."""
    cats = (
        [c.strip() for c in categories if c.strip()]
        if isinstance(categories, list)
        else (categories or "").split()
    )
    if any(cat in CORE_AI_CATEGORIES for cat in cats):
        return True

    if cats and not any(cat.startswith(RESCUE_CATEGORY_PREFIXES) for cat in cats):
        return False

    combined = f"{title or ''}\n{abstract or ''}"
    return bool(_AI_TERM_RE.search(combined) and _BENCH_TERM_RE.search(combined))


def _parse_version_number(record: dict[str, Any]) -> int:
    versions = record.get("versions")
    if isinstance(versions, list) and versions:
        last = versions[-1]
        if isinstance(last, dict):
            ver_str = str(last.get("version", ""))
            m = re.search(r"(\d+)", ver_str)
            if m:
                return int(m.group(1))
    return 1


def _parse_published_date(record: dict[str, Any]) -> str | None:
    update_date = record.get("update_date")
    versions = record.get("versions")
    if isinstance(versions, list) and versions:
        created = versions[0].get("created") if isinstance(versions[0], dict) else None
        if isinstance(created, str) and created:
            for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S GMT"):
                try:
                    return datetime.strptime(created, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
    if isinstance(update_date, str) and len(update_date) >= 10:
        return update_date[:10]
    return None


def _upsert_paper_record(
    writer: SingleWriterQueue,
    *,
    arxiv_id: str,
    version_seen: int,
    title: str,
    abstract: str,
    categories: list[str],
    published_date: str | None,
    updated_date: str | None,
    is_withdrawn: bool = False,
) -> None:
    cat_json = json.dumps(categories)
    sha = compute_metadata_sha256(title, abstract, categories)

    def _op(cur: Any) -> None:
        cur.execute(
            """
            INSERT INTO papers (
                arxiv_id, latest_version_seen, is_withdrawn, version_drift,
                title, abstract, categories_json, published_date, updated_date, metadata_sha256
            ) VALUES (?, ?, ?, 0, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(arxiv_id) DO UPDATE SET
                latest_version_seen = MAX(COALESCE(papers.latest_version_seen, 0), excluded.latest_version_seen),
                is_withdrawn = MAX(papers.is_withdrawn, excluded.is_withdrawn),
                version_drift = CASE
                    WHEN (papers.metadata_sha256 IS NOT NULL AND papers.metadata_sha256 != excluded.metadata_sha256)
                      OR (COALESCE(papers.latest_version_seen, 0) > 0 AND excluded.latest_version_seen > papers.latest_version_seen)
                    THEN 1 ELSE papers.version_drift END,
                title = COALESCE(NULLIF(excluded.title, ''), papers.title),
                abstract = COALESCE(NULLIF(excluded.abstract, ''), papers.abstract),
                categories_json = COALESCE(excluded.categories_json, papers.categories_json),
                published_date = COALESCE(NULLIF(NULLIF(papers.published_date, ''), 'unknown'), excluded.published_date),
                updated_date = COALESCE(excluded.updated_date, papers.updated_date),
                metadata_sha256 = excluded.metadata_sha256
            """,
            (
                arxiv_id,
                version_seen,
                1 if is_withdrawn else 0,
                title,
                abstract,
                cat_json,
                published_date,
                updated_date,
                sha,
            ),
        )

    writer.submit(_op)


def download_snapshot_from_gcs(
    settings: Settings,
    destination: Path,
    *,
    blob_name: str = "metadata-v5/arxiv-metadata-oai.json",
    gcs_client: Any | None = None,
) -> Path:
    """Download weekly arXiv metadata JSONL snapshot from gs://arxiv-dataset/."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    client = gcs_client
    if client is None:
        from google.cloud import storage

        client = storage.Client(project=settings.gcp_requester_pays_project)
    bucket = client.bucket(
        settings.gcs_arxiv_bucket,
        user_project=settings.gcp_requester_pays_project,
    )
    blob = bucket.blob(blob_name)
    blob.download_to_filename(str(destination))
    return destination


def download_snapshot_from_kaggle(
    destination_dir: Path,
    *,
    dataset: str = "cornell-university/arxiv",
) -> Path:
    """Download weekly Cornell-University/arxiv JSONL metadata snapshot via Kaggle CLI."""
    destination_dir.mkdir(parents=True, exist_ok=True)
    kaggle_bin = shutil.which("kaggle")
    if not kaggle_bin:
        candidate = Path.home() / "miniconda3" / "bin" / "kaggle"
        if candidate.is_file():
            kaggle_bin = str(candidate)
    if not kaggle_bin:
        raise RuntimeError(
            "Kaggle CLI not found. Install kaggle or pass --snapshot-path explicitly."
        )
    subprocess.run(
        [
            kaggle_bin,
            "datasets",
            "download",
            "-d",
            dataset,
            "-p",
            str(destination_dir),
            "--unzip",
        ],
        check=True,
    )
    out = destination_dir / "arxiv-metadata-oai-snapshot.json"
    if not out.is_file():
        raise FileNotFoundError(f"Expected Kaggle snapshot at {out} after unzip.")
    return out


def sync_snapshot(
    settings: Settings,
    writer: SingleWriterQueue,
    *,
    snapshot_path: Path | None = None,
    apply_prefilter: bool = True,
    limit: int | None = None,
    gcs_client: Any | None = None,
) -> SyncStats:
    """Stream arXiv JSONL snapshot into SQLite, quarantining malformed/truncated lines."""
    stats = SyncStats(source="arxiv_snapshot_v5")
    local_path = snapshot_path
    temp_downloaded = False
    if local_path is None:
        if gcs_client is not None:
            local_path = settings.staging_dir / "arxiv-metadata-oai.json"
            download_snapshot_from_gcs(settings, local_path, gcs_client=gcs_client)
            temp_downloaded = True
        else:
            cache_dir = settings.db_path.parent / "cache"
            local_path = download_snapshot_from_kaggle(cache_dir)

    max_date = ""
    try:
        # Check trailing newline to detect truncated snapshot dumps
        with local_path.open("rb") as fb:
            fb.seek(0, 2)
            size = fb.tell()
            if size > 0:
                fb.seek(max(0, size - 1))
                ends_with_nl = fb.read(1) == b"\n"
            else:
                ends_with_nl = True

        with local_path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                stats.records_read += 1
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    stats.malformed_lines += 1
                    continue
                if not isinstance(rec, dict) or not rec.get("id"):
                    stats.malformed_lines += 1
                    continue

                raw_id = str(rec["id"])
                arxiv_id, parsed_ver = canonicalize_arxiv_id(raw_id)
                version_seen = parsed_ver or _parse_version_number(rec)
                title = " ".join(str(rec.get("title") or "").split())
                abstract = " ".join(str(rec.get("abstract") or "").split())
                categories = str(rec.get("categories") or "").split()
                comments = str(rec.get("comments") or "").lower()
                is_withdrawn = "withdrawn" in comments or "withdrawn" in abstract.lower()[:120]
                pub_date = _parse_published_date(rec)
                upd_date = str(rec.get("update_date") or pub_date or "")[:10] or None

                if upd_date and upd_date > max_date:
                    max_date = upd_date

                if apply_prefilter and not passes_stage0_prefilter(categories, title, abstract):
                    if limit and stats.records_read >= limit:
                        break
                    continue

                stats.prefilter_passed += 1
                _upsert_paper_record(
                    writer,
                    arxiv_id=arxiv_id,
                    version_seen=version_seen,
                    title=title,
                    abstract=abstract,
                    categories=categories,
                    published_date=pub_date,
                    updated_date=upd_date,
                    is_withdrawn=is_withdrawn,
                )
                stats.records_upserted += 1
                if limit and stats.records_read >= limit:
                    break

        if not ends_with_nl and stats.malformed_lines == 0 and stats.records_read > 0:
            # Record non-newline termination warning cursor note
            cursor_note = "warning:no_trailing_newline"
        else:
            cursor_note = "ok"

        stats.watermark_date = max_date or None
        now_iso = datetime.now(UTC).isoformat()
        writer.submit_sql(
            """
            INSERT INTO ingestion_checkpoints (source, watermark_date, cursor_state, malformed_lines, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(source) DO UPDATE SET
                watermark_date = COALESCE(excluded.watermark_date, ingestion_checkpoints.watermark_date),
                cursor_state = excluded.cursor_state,
                malformed_lines = excluded.malformed_lines,
                updated_at = excluded.updated_at
            """,
            (stats.source, stats.watermark_date, cursor_note, stats.malformed_lines, now_iso),
        )
        writer.flush()
    finally:
        if temp_downloaded and local_path.exists():
            local_path.unlink(missing_ok=True)

    return stats


def _parse_atom_feed(xml_text: str) -> tuple[int, list[dict[str, Any]]]:
    """Parse arXiv Atom XML response into (total_results, parsed_entries)."""
    root = ET.fromstring(xml_text)
    total_el = root.find("opensearch:totalResults", ATOM_NS)
    total_results = int(total_el.text.strip()) if (total_el is not None and total_el.text) else 0

    entries: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        id_el = entry.find("atom:id", ATOM_NS)
        if id_el is None or not id_el.text:
            continue
        arxiv_id, ver = canonicalize_arxiv_id(id_el.text)
        title_el = entry.find("atom:title", ATOM_NS)
        summary_el = entry.find("atom:summary", ATOM_NS)
        pub_el = entry.find("atom:published", ATOM_NS)
        upd_el = entry.find("atom:updated", ATOM_NS)
        cats = [
            c.attrib["term"] for c in entry.findall("atom:category", ATOM_NS) if "term" in c.attrib
        ]
        entries.append(
            {
                "arxiv_id": arxiv_id,
                "version": ver or 1,
                "title": " ".join((title_el.text or "").split()) if title_el is not None else "",
                "abstract": (
                    " ".join((summary_el.text or "").split()) if summary_el is not None else ""
                ),
                "categories": cats,
                "published_date": (pub_el.text or "")[:10] if pub_el is not None else None,
                "updated_date": (upd_el.text or "")[:10] if upd_el is not None else None,
            }
        )
    return total_results, entries


def sync_atom_delta(
    conn: Any,
    writer: SingleWriterQueue,
    *,
    lookback_days: int | None = None,
    queries: tuple[str, ...] = DEFAULT_ATOM_QUERIES,
    page_size: int = 500,
    delay_seconds: float = 3.0,
    session: requests.Session | None = None,
    now_utc: datetime | None = None,
) -> SyncStats:
    """Fetch category-scoped Atom API deltas since committed watermark with pagination checks."""
    stats = SyncStats(source="arxiv_atom_delta")
    now = now_utc or datetime.now(UTC)
    http = session or requests.Session()

    row = conn.execute(
        "SELECT watermark_date FROM ingestion_checkpoints WHERE source = ?",
        (stats.source,),
    ).fetchone()
    if lookback_days is not None:
        start_dt = now - timedelta(days=lookback_days)
    elif row and row["watermark_date"]:
        # Subtract 1-day overlap buffer so late postings are never dropped
        start_dt = datetime.fromisoformat(row["watermark_date"]).replace(tzinfo=UTC) - timedelta(
            days=1
        )
    else:
        start_dt = now - timedelta(days=7)

    # Split wide catchup windows (>7 days) into 4-day slices to stay well below arXiv's pagination cap
    windows: list[tuple[datetime, datetime]] = []
    if (now - start_dt) > timedelta(days=7):
        cur_start = start_dt
        while cur_start < now:
            cur_end = min(now, cur_start + timedelta(days=4))
            windows.append((cur_start, cur_end))
            cur_start = cur_end
    else:
        windows.append((start_dt, now))

    max_seen_date = ""
    request_count = 0

    for win_start, win_end in windows:
        start_str = win_start.strftime("%Y%m%d0000")
        end_str = win_end.strftime("%Y%m%d2359")
        for base_query in queries:
            full_query = f"({base_query}) AND submittedDate:[{start_str} TO {end_str}]"
            start_offset = 0
            expected_total: int | None = None
            fetched_for_query = 0

            while True:
                if request_count > 0 and delay_seconds > 0:
                    time.sleep(delay_seconds)
                request_count += 1
                resp: Any = None
                for attempt in range(4):
                    try:
                        resp = http.get(
                            "https://export.arxiv.org/api/query",
                            params={
                                "search_query": full_query,
                                "start": start_offset,
                                "max_results": page_size,
                                "sortBy": "submittedDate",
                                "sortOrder": "descending",
                            },
                            headers={
                                "User-Agent": "arxiv-bench/0.2 (personal AI benchmark research)"
                            },
                            timeout=60,
                        )
                        if (
                            getattr(resp, "status_code", 200) in (429, 500, 502, 503, 504)
                            and attempt < 3
                        ):
                            time.sleep(max(delay_seconds, 2.0) * (2**attempt))
                            continue
                        resp.raise_for_status()
                        break
                    except requests.RequestException:
                        if attempt < 3:
                            time.sleep(max(delay_seconds, 2.0) * (2**attempt))
                            continue
                        raise
                total_results, entries = _parse_atom_feed(resp.text)
                if expected_total is None:
                    expected_total = total_results

                if not entries:
                    break

                for item in entries:
                    stats.records_read += 1
                    fetched_for_query += 1
                    pub_date = item["published_date"]
                    upd_date = item["updated_date"] or pub_date
                    if upd_date and upd_date > max_seen_date:
                        max_seen_date = upd_date

                    if not passes_stage0_prefilter(
                        item["categories"], item["title"], item["abstract"]
                    ):
                        continue

                    stats.prefilter_passed += 1
                    _upsert_paper_record(
                        writer,
                        arxiv_id=item["arxiv_id"],
                        version_seen=item["version"],
                        title=item["title"],
                        abstract=item["abstract"],
                        categories=item["categories"],
                        published_date=pub_date,
                        updated_date=upd_date,
                    )
                    stats.records_upserted += 1

                start_offset += len(entries)
                if start_offset >= (expected_total or 0):
                    break

            if expected_total is not None and fetched_for_query < expected_total:
                stats.incomplete_pagination = True

    if not stats.incomplete_pagination:
        stats.watermark_date = max_seen_date or now.strftime("%Y-%m-%d")
        writer.submit_sql(
            """
            INSERT INTO ingestion_checkpoints (source, watermark_date, cursor_state, malformed_lines, updated_at)
            VALUES (?, ?, 'ok', 0, ?)
            ON CONFLICT(source) DO UPDATE SET
                watermark_date = excluded.watermark_date,
                cursor_state = 'ok',
                updated_at = excluded.updated_at
            """,
            (stats.source, stats.watermark_date, now.isoformat()),
        )
    else:
        # Preserve prior watermark so next sync retries the incomplete window
        writer.submit_sql(
            """
            INSERT INTO ingestion_checkpoints (source, watermark_date, cursor_state, malformed_lines, updated_at)
            VALUES (?, NULL, 'incomplete_pagination', 0, ?)
            ON CONFLICT(source) DO UPDATE SET
                cursor_state = 'incomplete_pagination',
                updated_at = excluded.updated_at
            """,
            (stats.source, now.isoformat()),
        )
    writer.flush()
    return stats
