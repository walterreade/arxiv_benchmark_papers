"""Read-only idempotent legacy importer from /mnt/filestore flat CSV/JSON into NVMe SQLite."""

from __future__ import annotations

import csv
import json
import os
import re
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from arxiv_bench.config import Settings, canonicalize_arxiv_id, compute_metadata_sha256
from arxiv_bench.db import init_db
from arxiv_bench.pdf_storage import PdfStorageManager
from arxiv_bench.religion import normalize_bias_target

_SNAPSHOT_ID_RE = re.compile(r'"id"\s*:\s*"([^"]+)"')

CSV_COLS_12 = (
    "filename",
    "date",
    "title",
    "page_count",
    "is_benchmark",
    "is_llm_related",
    "is_bias_related",
    "is_faith_ethics_related",
    "is_survey_review",
    "reference_count",
    "appendix_length",
    "reasoning",
)

CSV_COLS_16 = (
    "filename",
    "date",
    "title",
    "page_count",
    "is_benchmark",
    "is_llm_related",
    "is_bias_related",
    "is_faith_ethics_related",
    "is_survey_review",
    "bias_and_fairness",
    "moral_reasoning",
    "ethics",
    "religion",
    "reference_count",
    "appendix_length",
    "reasoning",
)

BOOL_KEYS = frozenset(
    {
        "is_benchmark",
        "is_llm_related",
        "is_bias_related",
        "is_faith_ethics_related",
        "is_survey_review",
        "bias_and_fairness",
        "moral_reasoning",
        "ethics",
        "religion",
    }
)

INT_KEYS = frozenset({"page_count", "reference_count", "appendix_length"})


@dataclass
class MigrationReport:
    """Detailed counts from running migrate_legacy."""

    csv_rows_12: int = 0
    csv_rows_16: int = 0
    csv_rows_malformed: int = 0
    stage2_json_imported: int = 0
    stage2_quarantined: int = 0
    stage3_papers_imported: int = 0
    stage3_targets_imported: int = 0
    stage3_quarantined: int = 0
    stage4_imported: int = 0
    stage4_quarantined: int = 0
    legacy_cache_positives: int = 0
    legacy_cache_negatives_for_known_papers: int = 0
    legacy_cache_negatives_untracked: int = 0
    citations_imported: int = 0
    bug_failures_requeued: int = 0
    gcs_pdfs_indexed: int = 0
    snapshot_enriched: int = 0


def _parse_bool(val: Any) -> bool | None:
    if isinstance(val, bool):
        return val
    if val is None:
        return None
    s = str(val).strip().lower()
    if s == "true":
        return True
    if s == "false":
        return False
    return None


def _parse_int(val: Any) -> int | None:
    if isinstance(val, int) and not isinstance(val, bool):
        return val
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def _is_raw_response_poison(data: dict[str, Any]) -> bool:
    if "raw_response" not in data:
        return False
    meaningful = set(data.keys()) - {"raw_response", "filename", "title", "arxiv_url"}
    return len(meaningful) == 0


def _read_json_file(path: str) -> tuple[str, dict[str, Any] | None, str | None]:
    try:
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
        if not isinstance(obj, dict):
            return path, None, "top-level JSON is not an object"
        return path, obj, None
    except Exception as exc:  # noqa: BLE001
        return path, None, str(exc)


def _scan_json_paths(directory: Path) -> list[str]:
    if not directory.is_dir():
        return []
    return [
        ent.path for ent in os.scandir(directory) if ent.name.endswith(".json") and ent.is_file()
    ]


def parse_legacy_csv_row(row: list[str]) -> tuple[dict[str, Any] | None, int]:
    """Repair the 12-column vs 16-column schema shift in utility_files/1st_pass_results.csv."""
    width = len(row)
    if width == 12:
        mapping = dict(zip(CSV_COLS_12, row, strict=True))
    elif width == 16:
        mapping = dict(zip(CSV_COLS_16, row, strict=True))
    else:
        return None, width

    parsed: dict[str, Any] = {}
    for k, v in mapping.items():
        if k in BOOL_KEYS:
            parsed[k] = _parse_bool(v)
        elif k in INT_KEYS:
            parsed[k] = _parse_int(v)
        else:
            parsed[k] = v.strip()
    return parsed, width


def migrate_legacy(
    legacy_root: Path,
    settings: Settings,
    *,
    index_gcs: bool = False,
    gcs_client: Any | None = None,
    io_workers: int = 16,
    dry_run: bool = False,
) -> MigrationReport:
    """Idempotently import all legacy flat CSV/JSON data from legacy_root (read-only) into SQLite."""
    report = MigrationReport()
    now_iso = datetime.now(UTC).isoformat()

    # Step 1: Parse utility_files/1st_pass_results.csv repairing 12-col vs 16-col shift
    csv_by_id: dict[str, dict[str, Any]] = {}
    csv_path = legacy_root / "utility_files" / "1st_pass_results.csv"
    if csv_path.is_file():
        with csv_path.open("r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip 12-col header
            for row in reader:
                if not row:
                    continue
                parsed, width = parse_legacy_csv_row(row)
                if parsed is None:
                    report.csv_rows_malformed += 1
                    continue
                if width == 12:
                    report.csv_rows_12 += 1
                else:
                    report.csv_rows_16 += 1
                aid, _ = canonicalize_arxiv_id(parsed["filename"])
                csv_by_id[aid] = parsed

    if dry_run:
        return report

    conn = init_db(settings.db_path)
    try:
        cur = conn.cursor()

        # Insert CSV rows first so page_count & repaired metadata are present even if JSON missing
        cur.execute("BEGIN IMMEDIATE;")
        for aid, cdata in csv_by_id.items():
            cur.execute(
                """
                INSERT INTO papers (arxiv_id, title, published_date, page_count, legacy_metadata_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(arxiv_id) DO UPDATE SET
                    title = COALESCE(NULLIF(excluded.title, ''), papers.title),
                    published_date = COALESCE(NULLIF(excluded.published_date, ''), papers.published_date),
                    page_count = COALESCE(excluded.page_count, papers.page_count),
                    legacy_metadata_json = COALESCE(papers.legacy_metadata_json, excluded.legacy_metadata_json)
                """,
                (
                    aid,
                    cdata.get("title") or None,
                    cdata.get("date") or None,
                    cdata.get("page_count"),
                    json.dumps(cdata),
                ),
            )
        conn.commit()

        # Step 2: Import json/2_paper_metadata/*.json merged with CSV page_count
        s2_paths = _scan_json_paths(legacy_root / "json" / "2_paper_metadata")
        with ThreadPoolExecutor(max_workers=io_workers) as pool:
            cur.execute("BEGIN IMMEDIATE;")
            batch_n = 0
            for fpath, obj, err in pool.map(_read_json_file, s2_paths):
                aid, _ = canonicalize_arxiv_id(Path(fpath).stem)
                if obj is None or _is_raw_response_poison(obj):
                    report.stage2_quarantined += 1
                    cur.execute("INSERT OR IGNORE INTO papers (arxiv_id) VALUES (?)", (aid,))
                    detail = (
                        err or str(obj.get("raw_response", ""))[:2000]
                        if obj
                        else (err or "invalid")
                    )
                    cur.execute(
                        """
                        INSERT INTO paper_stage_status (
                            arxiv_id, stage, status, attempt_count,
                            last_error_code, last_error_detail, updated_at
                        ) VALUES (?, 'legacy_stage2', 'quarantined_invalid_schema', 1, 'RAW_RESPONSE', ?, ?)
                        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                            status = 'quarantined_invalid_schema',
                            last_error_detail = excluded.last_error_detail,
                            updated_at = excluded.updated_at
                        """,
                        (aid, detail, now_iso),
                    )
                else:
                    merged = dict(csv_by_id.get(aid, {}))
                    merged.update(obj)
                    title = str(merged.get("title") or "").strip() or None
                    pub_date = str(merged.get("date") or "").strip() or None
                    page_count = _parse_int(merged.get("page_count"))
                    cur.execute(
                        """
                        INSERT INTO papers (arxiv_id, title, published_date, page_count, legacy_metadata_json)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(arxiv_id) DO UPDATE SET
                            title = COALESCE(excluded.title, papers.title),
                            published_date = COALESCE(excluded.published_date, papers.published_date),
                            page_count = COALESCE(excluded.page_count, papers.page_count),
                            legacy_metadata_json = excluded.legacy_metadata_json
                        """,
                        (aid, title, pub_date, page_count, json.dumps(merged)),
                    )
                    report.stage2_json_imported += 1

                batch_n += 1
                if batch_n >= 1000:
                    conn.commit()
                    cur.execute("BEGIN IMMEDIATE;")
                    batch_n = 0
            conn.commit()

        # Step 3: Import json/3_paper_bias_targets/*.json handling polymorphic list[str] & list[dict]
        s3_paths = _scan_json_paths(legacy_root / "json" / "3_paper_bias_targets")
        with ThreadPoolExecutor(max_workers=io_workers) as pool:
            cur.execute("BEGIN IMMEDIATE;")
            batch_n = 0
            for fpath, obj, err in pool.map(_read_json_file, s3_paths):
                aid, _ = canonicalize_arxiv_id(Path(fpath).stem)
                if obj is None or _is_raw_response_poison(obj):
                    report.stage3_quarantined += 1
                    cur.execute("INSERT OR IGNORE INTO papers (arxiv_id) VALUES (?)", (aid,))
                    detail = err or str((obj or {}).get("raw_response", ""))[:2000]
                    cur.execute(
                        """
                        INSERT INTO paper_stage_status (
                            arxiv_id, stage, status, attempt_count,
                            last_error_code, last_error_detail, updated_at
                        ) VALUES (?, 'religion_bias_targets', 'quarantined_invalid_schema', 1, 'RAW_RESPONSE', ?, ?)
                        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                            status = 'quarantined_invalid_schema',
                            last_error_detail = excluded.last_error_detail,
                            updated_at = excluded.updated_at
                        """,
                        (aid, detail, now_iso),
                    )
                else:
                    title = str(obj.get("title") or "").strip() or None
                    cur.execute(
                        """
                        INSERT INTO papers (arxiv_id, title) VALUES (?, ?)
                        ON CONFLICT(arxiv_id) DO UPDATE SET title = COALESCE(papers.title, excluded.title)
                        """,
                        (aid, title),
                    )
                    raw_primary = str(obj.get("primary_bias_target") or "").strip()
                    norm_primary = normalize_bias_target(raw_primary) if raw_primary else ""
                    cur.execute("DELETE FROM paper_bias_targets WHERE arxiv_id = ?", (aid,))
                    raw_targets = obj.get("bias_targets") or []
                    if isinstance(raw_targets, list):
                        for entry in raw_targets:
                            if isinstance(entry, dict):
                                t_raw = str(entry.get("target") or "").strip()
                                meth = str(entry.get("methodology") or "").strip()
                            else:
                                t_raw = str(entry or "").strip()
                                meth = ""
                            if not t_raw:
                                continue
                            t_norm = normalize_bias_target(t_raw)
                            is_prim = (
                                1 if norm_primary and t_norm.lower() == norm_primary.lower() else 0
                            )
                            cur.execute(
                                """
                                INSERT OR IGNORE INTO paper_bias_targets (arxiv_id, target, methodology, is_primary)
                                VALUES (?, ?, ?, ?)
                                """,
                                (aid, t_norm, meth, is_prim),
                            )
                            report.stage3_targets_imported += 1
                    cur.execute(
                        """
                        INSERT INTO paper_stage_status (
                            arxiv_id, stage, status, attempt_count, run_id, updated_at
                        ) VALUES (?, 'religion_bias_targets', 'done', 1, 'legacy_import', ?)
                        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                            status = 'done',
                            updated_at = excluded.updated_at
                        """,
                        (aid, now_iso),
                    )
                    report.stage3_papers_imported += 1

                batch_n += 1
                if batch_n >= 1000:
                    conn.commit()
                    cur.execute("BEGIN IMMEDIATE;")
                    batch_n = 0
            conn.commit()

        # Step 4: Import json/4_religious_bias_analysis/*.json normalizing benchmark_measurement
        s4_paths = _scan_json_paths(legacy_root / "json" / "4_religious_bias_analysis")
        with ThreadPoolExecutor(max_workers=io_workers) as pool:
            cur.execute("BEGIN IMMEDIATE;")
            for fpath, obj, err in pool.map(_read_json_file, s4_paths):
                aid, _ = canonicalize_arxiv_id(Path(fpath).stem)
                if obj is None or _is_raw_response_poison(obj):
                    report.stage4_quarantined += 1
                    cur.execute("INSERT OR IGNORE INTO papers (arxiv_id) VALUES (?)", (aid,))
                    detail = err or str((obj or {}).get("raw_response", ""))[:2000]
                    cur.execute(
                        """
                        INSERT INTO paper_stage_status (
                            arxiv_id, stage, status, attempt_count,
                            last_error_code, last_error_detail, updated_at
                        ) VALUES (?, 'religion_extract', 'quarantined_invalid_schema', 1, 'RAW_RESPONSE', ?, ?)
                        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                            status = 'quarantined_invalid_schema',
                            last_error_detail = excluded.last_error_detail,
                            updated_at = excluded.updated_at
                        """,
                        (aid, detail, now_iso),
                    )
                    continue

                title = str(obj.get("title") or "").strip() or None
                cur.execute(
                    """
                    INSERT INTO papers (arxiv_id, title) VALUES (?, ?)
                    ON CONFLICT(arxiv_id) DO UPDATE SET title = COALESCE(papers.title, excluded.title)
                    """,
                    (aid, title),
                )
                measurement = (
                    obj.get("measurement_description") or obj.get("benchmark_measurement") or ""
                )
                rel_comp = str(obj.get("religion_component") or "none").strip().lower()
                cont_test = 1 if _parse_bool(obj.get("continuous_testing")) else 0

                def _as_list(val: Any) -> list[str]:
                    if isinstance(val, list):
                        return [str(x).strip() for x in val if str(x).strip()]
                    if isinstance(val, str) and val.strip():
                        return [val.strip()]
                    return []

                cur.execute(
                    """
                    INSERT INTO religious_bias_details (
                        arxiv_id, religion_component, measurement_description,
                        religious_groups_json, models_tested_json, languages_json,
                        response_type_json, base_benchmarks_json, continuous_testing,
                        findings, extracted_at, run_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'legacy_import')
                    ON CONFLICT(arxiv_id) DO UPDATE SET
                        religion_component = excluded.religion_component,
                        measurement_description = excluded.measurement_description,
                        religious_groups_json = excluded.religious_groups_json,
                        models_tested_json = excluded.models_tested_json,
                        languages_json = excluded.languages_json,
                        response_type_json = excluded.response_type_json,
                        base_benchmarks_json = excluded.base_benchmarks_json,
                        continuous_testing = excluded.continuous_testing,
                        findings = excluded.findings
                    """,
                    (
                        aid,
                        rel_comp,
                        str(measurement),
                        json.dumps(_as_list(obj.get("religious_groups"))),
                        json.dumps(_as_list(obj.get("models_tested"))),
                        json.dumps(_as_list(obj.get("languages_evaluated"))),
                        json.dumps(_as_list(obj.get("response_type"))),
                        json.dumps(_as_list(obj.get("base_benchmarks"))),
                        cont_test,
                        str(obj.get("findings") or ""),
                        now_iso,
                    ),
                )
                cur.execute(
                    """
                    INSERT INTO paper_stage_status (arxiv_id, stage, status, attempt_count, run_id, updated_at)
                    VALUES (?, 'religion_extract', 'done', 1, 'legacy_import', ?)
                    ON CONFLICT(arxiv_id, stage) DO UPDATE SET status = 'done', updated_at = excluded.updated_at
                    """,
                    (aid, now_iso),
                )
                report.stage4_imported += 1
            conn.commit()

        # Step 5: Import download_assessments_cache.json stamped under legacy_llm_bias_v1
        cache_path = legacy_root / "utility_files" / "download_assessments_cache.json"
        if cache_path.is_file():
            known_ids = {str(r[0]) for r in conn.execute("SELECT arxiv_id FROM papers").fetchall()}
            cache_data = json.loads(cache_path.read_text(encoding="utf-8"))
            if isinstance(cache_data, dict):
                cur.execute("BEGIN IMMEDIATE;")
                batch_n = 0
                for raw_id, flag in cache_data.items():
                    aid, _ = canonicalize_arxiv_id(str(raw_id))
                    is_pos = bool(flag)
                    if is_pos:
                        if aid not in known_ids:
                            cur.execute(
                                "INSERT OR IGNORE INTO papers (arxiv_id) VALUES (?)", (aid,)
                            )
                            known_ids.add(aid)
                        cur.execute(
                            """
                            INSERT INTO triage_assessments (
                                arxiv_id, paper_version, rubric_id, rubric_version,
                                question_id, model_id, choice_or_bool, probability, assessed_at
                            ) VALUES (?, 0, 'legacy_llm_bias', 'legacy_llm_bias_v1', 'is_relevant', 'legacy_flash', 'true', 1.0, ?)
                            ON CONFLICT(arxiv_id, paper_version, rubric_id, rubric_version, question_id)
                            DO UPDATE SET choice_or_bool = excluded.choice_or_bool, probability = excluded.probability
                            """,
                            (aid, now_iso),
                        )
                        report.legacy_cache_positives += 1
                        batch_n += 1
                    elif aid in known_ids:
                        cur.execute(
                            """
                            INSERT INTO triage_assessments (
                                arxiv_id, paper_version, rubric_id, rubric_version,
                                question_id, model_id, choice_or_bool, probability, assessed_at
                            ) VALUES (?, 0, 'legacy_llm_bias', 'legacy_llm_bias_v1', 'is_relevant', 'legacy_flash', 'false', 0.0, ?)
                            ON CONFLICT(arxiv_id, paper_version, rubric_id, rubric_version, question_id)
                            DO UPDATE SET choice_or_bool = excluded.choice_or_bool, probability = excluded.probability
                            """,
                            (aid, now_iso),
                        )
                        report.legacy_cache_negatives_for_known_papers += 1
                        batch_n += 1
                    else:
                        report.legacy_cache_negatives_untracked += 1

                    if batch_n >= 2000:
                        conn.commit()
                        cur.execute("BEGIN IMMEDIATE;")
                        batch_n = 0
                conn.commit()

        # Step 6: Import valid citations_cache.json entries
        cites_path = legacy_root / "utility_files" / "citations_cache.json"
        if cites_path.is_file():
            cites = json.loads(cites_path.read_text(encoding="utf-8"))
            if isinstance(cites, dict):
                cur.execute("BEGIN IMMEDIATE;")
                for raw_id, entry in cites.items():
                    if not isinstance(entry, dict):
                        continue
                    cnt = _parse_int(entry.get("count"))
                    ts = str(entry.get("timestamp") or now_iso)
                    if cnt is None:
                        continue
                    aid, _ = canonicalize_arxiv_id(str(raw_id))
                    cur.execute(
                        """
                        UPDATE papers
                        SET citation_count = COALESCE(citation_count, ?),
                            s2_fetched_at = COALESCE(s2_fetched_at, ?)
                        WHERE arxiv_id = ?
                        """,
                        (cnt, ts, aid),
                    )
                    if cur.rowcount > 0:
                        report.citations_imported += 1
                conn.commit()

        # Step 7: Requeue transient code-bug failures from 2nd_pass_failures & 3rd_pass_failures
        failure_files = (
            ("2nd_pass_failures.csv", "religion_bias_targets"),
            ("3rd_pass_failures.csv", "religion_extract"),
        )
        requeued_seen: set[tuple[str, str]] = set()
        cur.execute("BEGIN IMMEDIATE;")
        for fname, stage_name in failure_files:
            fpath = legacy_root / "utility_files" / fname
            if not fpath.is_file():
                continue
            with fpath.open("r", encoding="utf-8", errors="replace", newline="") as f:
                for row in csv.DictReader(f):
                    raw_fn = row.get("filename") or ""
                    err_txt = row.get("error") or ""
                    if not raw_fn:
                        continue
                    if "'list' object is not a mapping" in err_txt or "NoneType" in err_txt:
                        aid, _ = canonicalize_arxiv_id(raw_fn)
                        if (aid, stage_name) in requeued_seen:
                            continue
                        requeued_seen.add((aid, stage_name))
                        cur.execute("INSERT OR IGNORE INTO papers (arxiv_id) VALUES (?)", (aid,))
                        # Only requeue if not already cleanly extracted
                        cur.execute(
                            """
                            INSERT INTO paper_stage_status (
                                arxiv_id, stage, status, attempt_count,
                                last_error_code, last_error_detail, updated_at
                            ) VALUES (?, ?, 'pending', 0, 'REQUEUED_LEGACY_BUG', ?, ?)
                            ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                                status = CASE
                                    WHEN paper_stage_status.status = 'done' THEN 'done'
                                    ELSE 'pending'
                                END,
                                last_error_code = CASE
                                    WHEN paper_stage_status.status = 'done'
                                    THEN paper_stage_status.last_error_code
                                    ELSE 'REQUEUED_LEGACY_BUG'
                                END,
                                last_error_detail = CASE
                                    WHEN paper_stage_status.status = 'done'
                                    THEN paper_stage_status.last_error_detail
                                    ELSE excluded.last_error_detail
                                END,
                                updated_at = excluded.updated_at
                            """,
                            (aid, stage_name, err_txt[:500], now_iso),
                        )
                        report.bug_failures_requeued += 1
        conn.commit()

        # Step 8: Optionally index existing gs://inversion/pdf/ objects once
        if index_gcs:
            storage = PdfStorageManager(settings, gcs_client=gcs_client)
            report.gcs_pdfs_indexed = storage.index_existing_gcs_pdfs(conn)

        # Step 9: Enrich existing papers with categories/abstract/authors from local legacy snapshot
        snapshot_path = legacy_root / "utility_files" / "arxiv-metadata-oai-snapshot.json"
        if snapshot_path.is_file():
            report.snapshot_enriched = backfill_legacy_snapshot_metadata(conn, snapshot_path)
    finally:
        conn.close()

    return report


def backfill_legacy_snapshot_metadata(
    conn: sqlite3.Connection,
    snapshot_path: Path,
) -> int:
    """Stream local legacy arXiv snapshot once to fill missing categories/abstract/authors."""
    needed = {
        str(r[0])
        for r in conn.execute(
            "SELECT arxiv_id FROM papers WHERE categories_json IS NULL OR abstract IS NULL"
        ).fetchall()
    }
    if not needed or not snapshot_path.is_file():
        return 0

    enriched = 0
    batch: list[tuple[Any, ...]] = []
    with snapshot_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = _SNAPSHOT_ID_RE.search(line[:200])
            if not m:
                continue
            aid, _ = canonicalize_arxiv_id(m.group(1))
            if aid not in needed:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            cats = [c for c in str(rec.get("categories") or "").split() if c]
            title = " ".join(str(rec.get("title") or "").split()) or None
            abstract = " ".join(str(rec.get("abstract") or "").split()) or None
            versions = rec.get("versions") or []
            latest_ver = len(versions) if isinstance(versions, list) and versions else 1
            upd_date = str(rec.get("update_date") or "").strip() or None
            meta_sha = compute_metadata_sha256(title, abstract, cats)
            batch.append(
                (
                    title,
                    abstract,
                    json.dumps(cats) if cats else None,
                    upd_date,
                    latest_ver,
                    meta_sha,
                    aid,
                )
            )
            needed.discard(aid)
            if len(batch) >= 1000:
                enriched += _apply_snapshot_batch(conn, batch)
                batch.clear()
            if not needed:
                break

    if batch:
        enriched += _apply_snapshot_batch(conn, batch)
    return enriched


def _apply_snapshot_batch(conn: sqlite3.Connection, batch: list[tuple[Any, ...]]) -> int:
    cur = conn.cursor()
    cur.execute("BEGIN IMMEDIATE;")
    cur.executemany(
        """
        UPDATE papers
        SET title = COALESCE(papers.title, ?),
            abstract = COALESCE(papers.abstract, ?),
            categories_json = COALESCE(papers.categories_json, ?),
            updated_date = COALESCE(papers.updated_date, ?),
            latest_version_seen = MAX(COALESCE(papers.latest_version_seen, 1), ?),
            metadata_sha256 = COALESCE(papers.metadata_sha256, ?)
        WHERE arxiv_id = ?
        """,
        batch,
    )
    conn.commit()
    return len(batch)
