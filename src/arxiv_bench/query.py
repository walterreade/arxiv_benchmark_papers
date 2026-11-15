"""Exploratory gap-analysis search, coverage matrices, alias merges, BibTeX, and health status."""

from __future__ import annotations

import csv
import io
import json
import re
import shutil
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from arxiv_bench.config import Settings, get_arxiv_url

_FTS_OPERATORS = frozenset({"AND", "OR", "NOT"})
_FTS_SPECIAL_RE = re.compile(r"[-:/.*^+()~]")
_TOKEN_RE = re.compile(r'"[^"]+"|\S+')

ALLOWED_MATRIX_DIMS = frozenset(
    {
        "modality",
        "domain",
        "task",
        "contribution_type",
        "year",
        "evaluation_method",
    }
)


@dataclass(frozen=True)
class MergeReport:
    """Result counts for a manual transactional entity alias merge."""

    source_id: str
    target_id: str
    aliases_moved: int
    benchmarks_updated: int
    models_updated: int


@dataclass
class CoverageMatrix:
    """Two-dimensional cross-tabulation highlighting sparse benchmark gap cells."""

    rows_dim: str
    cols_dim: str
    row_labels: list[str]
    col_labels: list[str]
    counts: dict[tuple[str, str], int]
    zero_cells: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class StatusReport:
    """Operational status snapshot with stale-watermark and disk health alerts."""

    db_path: str
    db_size_mb: float
    nvme_free_gb: float
    total_papers: int
    triaged_papers: int
    extracted_benchmarks: int
    religion_papers: int
    decision_score_rows: int
    pending_pdf_uploads: int
    quarantined_papers: int
    stage_counts: dict[str, dict[str, int]]
    watermarks: dict[str, dict[str, Any]]
    last_backup_at: str | None
    alerts: list[str]


def sanitize_fts5_query(raw_query: str) -> str:
    """Escape FTS5 special characters (e.g., 'SWE-bench', 'agent:tool', 'v2.0') safely."""
    tokens = _TOKEN_RE.findall(raw_query.strip())
    if not tokens:
        return ""
    out: list[str] = []
    for tok in tokens:
        if tok.startswith('"') and tok.endswith('"'):
            out.append(tok)
        elif tok in _FTS_OPERATORS and out:
            out.append(tok)
        elif _FTS_SPECIAL_RE.search(tok):
            escaped = tok.replace('"', '""')
            out.append(f'"{escaped}"')
        else:
            out.append(tok)
    return " ".join(out)


def search_papers(
    conn: sqlite3.Connection,
    query: str,
    *,
    modality: str | None = None,
    domain: str | None = None,
    contribution_type: str | None = None,
    rubric_filter: tuple[str, str, str] | None = None,
    religion_only: bool = False,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Run sanitized FTS5 BM25 search with optional normalized facet and rubric filters."""
    safe_query = sanitize_fts5_query(query)
    if not safe_query:
        return []

    joins: list[str] = ["INNER JOIN papers_fts fts ON fts.rowid = p.rowid"]
    wheres: list[str] = ["papers_fts MATCH ?"]
    params: list[Any] = [safe_query]

    if modality:
        joins.append("INNER JOIN paper_modalities pm ON pm.arxiv_id = p.arxiv_id")
        wheres.append("pm.modality = ?")
        params.append(modality.strip().lower())
    if domain:
        joins.append("INNER JOIN paper_domains pd ON pd.arxiv_id = p.arxiv_id")
        wheres.append("pd.domain = ?")
        params.append(domain.strip().lower())
    if contribution_type:
        wheres.append("json_extract(p.extraction_json, '$.contribution_type') = ?")
        params.append(contribution_type.strip())
    if religion_only:
        joins.append("INNER JOIN religious_bias_details r ON r.arxiv_id = p.arxiv_id")
    if rubric_filter:
        rubric_spec, question_id, choice_val = rubric_filter
        if "@" in rubric_spec:
            rubric_id, rubric_ver = rubric_spec.split("@", 1)
            wheres.append(
                """
                EXISTS (
                    SELECT 1 FROM decision_scores ds
                    WHERE ds.arxiv_id = p.arxiv_id
                      AND ds.rubric_id = ?
                      AND ds.rubric_version = ?
                      AND ds.question_id = ?
                      AND ds.choice_or_score = ?
                )
                """
            )
            params.extend([rubric_id.strip(), rubric_ver.strip(), question_id, choice_val])
        else:
            wheres.append(
                """
                p.arxiv_id IN (
                    SELECT arxiv_id
                    FROM (
                        SELECT arxiv_id, choice_or_score,
                               ROW_NUMBER() OVER (
                                   PARTITION BY arxiv_id
                                   ORDER BY scored_at DESC, rubric_version DESC
                               ) AS rn
                        FROM decision_scores
                        WHERE rubric_id = ? AND question_id = ?
                    )
                    WHERE rn = 1 AND choice_or_score = ?
                )
                """
            )
            params.extend([rubric_spec.strip(), question_id, choice_val])

    sql = f"""
        SELECT DISTINCT
            p.arxiv_id,
            p.title,
            p.published_date,
            p.venue,
            p.citation_count,
            p.gcs_pdf_uri,
            json_extract(p.extraction_json, '$.contribution_type') AS contribution_type,
            p.evidence_card,
            bm25(papers_fts) AS rank_score
        FROM papers p
        {" ".join(joins)}
        WHERE {" AND ".join(wheres)}
        ORDER BY rank_score ASC, COALESCE(p.citation_count, 0) DESC
        LIMIT ?
    """
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def _dimension_subquery(dim: str) -> tuple[str, list[Any]]:
    """Return (SQL producing (arxiv_id, label), params) for a coverage-matrix axis."""
    if ":" in dim:
        rubric_spec, question_id = dim.split(":", 1)
        if "@" in rubric_spec:
            rubric_id, rubric_ver = rubric_spec.split("@", 1)
            return (
                """
                SELECT arxiv_id, choice_or_score AS label
                FROM decision_scores
                WHERE rubric_id = ? AND rubric_version = ? AND question_id = ?
                """,
                [rubric_id.strip(), rubric_ver.strip(), question_id.strip()],
            )
        return (
            """
            SELECT arxiv_id, choice_or_score AS label
            FROM (
                SELECT arxiv_id, choice_or_score,
                       ROW_NUMBER() OVER (
                           PARTITION BY arxiv_id
                           ORDER BY scored_at DESC, rubric_version DESC
                       ) AS rn
                FROM decision_scores
                WHERE rubric_id = ? AND question_id = ?
            )
            WHERE rn = 1
            """,
            [rubric_spec.strip(), question_id.strip()],
        )

    if dim == "modality":
        return "SELECT arxiv_id, modality AS label FROM paper_modalities", []
    if dim == "domain":
        return "SELECT arxiv_id, domain AS label FROM paper_domains", []
    if dim == "task":
        return "SELECT arxiv_id, task AS label FROM paper_tasks", []
    if dim == "contribution_type":
        return (
            """
            SELECT arxiv_id, json_extract(extraction_json, '$.contribution_type') AS label
            FROM papers
            WHERE extraction_json IS NOT NULL
            """,
            [],
        )
    if dim == "year":
        return (
            """
            SELECT arxiv_id, substr(published_date, 1, 4) AS label
            FROM papers
            WHERE published_date IS NOT NULL AND length(published_date) >= 4
            """,
            [],
        )
    if dim == "evaluation_method":
        return (
            """
            SELECT p.arxiv_id, lower(trim(je.value)) AS label
            FROM papers p, json_each(p.extraction_json, '$.evaluation_methods') je
            WHERE p.extraction_json IS NOT NULL
            """,
            [],
        )
    raise ValueError(
        f"Unsupported matrix dimension '{dim}'. Choose one of {sorted(ALLOWED_MATRIX_DIMS)} "
        "or '<rubric_id>:<question_id>'."
    )


def build_coverage_matrix(
    conn: sqlite3.Connection,
    rows_dim: str,
    cols_dim: str,
    *,
    domain: str | None = None,
    modality: str | None = None,
    year_from: int | None = None,
) -> CoverageMatrix:
    """Cross-tabulate two benchmark dimensions to identify sparse coverage gap cells."""
    r_sql, r_params = _dimension_subquery(rows_dim)
    c_sql, c_params = _dimension_subquery(cols_dim)

    filters: list[str] = ["p.extraction_json IS NOT NULL"]
    f_params: list[Any] = []
    extra_joins: list[str] = []

    if domain:
        extra_joins.append("INNER JOIN paper_domains fdom ON fdom.arxiv_id = p.arxiv_id")
        filters.append("fdom.domain = ?")
        f_params.append(domain.strip().lower())
    if modality:
        extra_joins.append("INNER JOIN paper_modalities fmod ON fmod.arxiv_id = p.arxiv_id")
        filters.append("fmod.modality = ?")
        f_params.append(modality.strip().lower())
    if year_from is not None:
        filters.append("CAST(substr(COALESCE(p.published_date, '0000'), 1, 4) AS INTEGER) >= ?")
        f_params.append(year_from)

    sql = f"""
        WITH row_axis AS ({r_sql}),
             col_axis AS ({c_sql})
        SELECT r.label AS row_label, c.label AS col_label, COUNT(DISTINCT p.arxiv_id) AS cnt
        FROM papers p
        INNER JOIN row_axis r ON r.arxiv_id = p.arxiv_id
        INNER JOIN col_axis c ON c.arxiv_id = p.arxiv_id
        {" ".join(extra_joins)}
        WHERE {" AND ".join(filters)}
          AND r.label IS NOT NULL AND r.label != ''
          AND c.label IS NOT NULL AND c.label != ''
        GROUP BY r.label, c.label
    """
    rows = conn.execute(sql, r_params + c_params + f_params).fetchall()
    counts: dict[tuple[str, str], int] = {}
    row_totals: dict[str, int] = {}
    col_totals: dict[str, int] = {}

    for rec in rows:
        rl = str(rec["row_label"])
        cl = str(rec["col_label"])
        cnt = int(rec["cnt"])
        counts[(rl, cl)] = cnt
        row_totals[rl] = row_totals.get(rl, 0) + cnt
        col_totals[cl] = col_totals.get(cl, 0) + cnt

    row_labels = sorted(row_totals.keys(), key=lambda k: (-row_totals[k], k))
    col_labels = sorted(col_totals.keys(), key=lambda k: (-col_totals[k], k))
    zero_cells = [
        (rl, cl) for rl in row_labels for cl in col_labels if counts.get((rl, cl), 0) == 0
    ]
    return CoverageMatrix(
        rows_dim=rows_dim,
        cols_dim=cols_dim,
        row_labels=row_labels,
        col_labels=col_labels,
        counts=counts,
        zero_cells=zero_cells,
    )


def merge_entity_aliases(
    conn: sqlite3.Connection,
    source_id: str,
    target_id: str,
) -> MergeReport:
    """Transactionally merge source_id into target_id without modifying raw extraction JSON."""
    if source_id == target_id:
        raise ValueError("source_id and target_id must differ.")

    src = conn.execute("SELECT * FROM entities WHERE canonical_id = ?", (source_id,)).fetchone()
    dst = conn.execute("SELECT * FROM entities WHERE canonical_id = ?", (target_id,)).fetchone()
    if src is None:
        raise ValueError(f"Source entity '{source_id}' not found.")
    if dst is None:
        raise ValueError(f"Target entity '{target_id}' not found.")
    if src["entity_type"] != dst["entity_type"]:
        raise ValueError(
            f"Cannot merge mismatched entity types: '{src['entity_type']}' vs '{dst['entity_type']}'."
        )

    cur = conn.cursor()
    cur.execute("BEGIN IMMEDIATE;")
    try:
        # Preserve URL/S2 metadata on target if missing
        cur.execute(
            """
            UPDATE entities
            SET canonical_url = COALESCE(canonical_url, ?),
                s2_paper_id = COALESCE(s2_paper_id, ?)
            WHERE canonical_id = ?
            """,
            (src["canonical_url"], src["s2_paper_id"], target_id),
        )

        # Re-point aliases
        cur.execute(
            """
            UPDATE entity_aliases
            SET canonical_id = ?, resolution_method = 'manual_merge'
            WHERE canonical_id = ?
            """,
            (target_id, source_id),
        )
        aliases_moved = cur.rowcount

        # Deduplicate & re-point paper_benchmarks
        cur.execute(
            """
            INSERT OR IGNORE INTO paper_benchmarks (arxiv_id, canonical_id, role)
            SELECT arxiv_id, ?, role FROM paper_benchmarks WHERE canonical_id = ?
            """,
            (target_id, source_id),
        )
        cur.execute("DELETE FROM paper_benchmarks WHERE canonical_id = ?", (source_id,))
        benchmarks_updated = cur.rowcount

        # Deduplicate & re-point paper_models
        cur.execute(
            """
            INSERT OR IGNORE INTO paper_models (arxiv_id, canonical_id)
            SELECT arxiv_id, ? FROM paper_models WHERE canonical_id = ?
            """,
            (target_id, source_id),
        )
        cur.execute("DELETE FROM paper_models WHERE canonical_id = ?", (source_id,))
        models_updated = cur.rowcount

        cur.execute("DELETE FROM entities WHERE canonical_id = ?", (source_id,))
        conn.commit()
    except BaseException:
        conn.rollback()
        raise

    return MergeReport(
        source_id=source_id,
        target_id=target_id,
        aliases_moved=aliases_moved,
        benchmarks_updated=benchmarks_updated,
        models_updated=models_updated,
    )


def format_bibtex(paper: dict[str, Any]) -> str:
    """Format a paper row as a clean BibTeX entry."""
    arxiv_id = str(paper.get("arxiv_id") or "unknown")
    title = str(paper.get("title") or "Untitled").replace("{", "\\{").replace("}", "\\}")
    pub_date = str(paper.get("published_date") or "")
    year = pub_date[:4] if len(pub_date) >= 4 and pub_date[:4].isdigit() else "YYYY"
    venue = str(paper.get("venue") or "").strip()
    url = get_arxiv_url(arxiv_id)

    title_words = re.findall(r"[a-zA-Z0-9]+", title.lower())
    keyword = next((w for w in title_words if len(w) > 3), "paper")
    safe_id = re.sub(r"[^a-zA-Z0-9]", "_", arxiv_id)
    key = f"arxiv_{safe_id}_{year}_{keyword}"

    if venue:
        return (
            f"@inproceedings{{{key},\n"
            f"  title={{{title}}},\n"
            f"  booktitle={{{venue}}},\n"
            f"  year={{{year}}},\n"
            f"  eprint={{{arxiv_id}}},\n"
            f"  archivePrefix={{arXiv}},\n"
            f"  url={{{url}}}\n"
            f"}}"
        )
    return (
        f"@misc{{{key},\n"
        f"  title={{{title}}},\n"
        f"  year={{{year}}},\n"
        f"  eprint={{{arxiv_id}}},\n"
        f"  archivePrefix={{arXiv}},\n"
        f"  url={{{url}}}\n"
        f"}}"
    )


def get_pipeline_status(
    conn: sqlite3.Connection,
    settings: Settings,
    *,
    now_utc: datetime | None = None,
    stale_hours: float = 48.0,
) -> StatusReport:
    """Compute operational health status and flag stale watermarks or low NVMe disk space."""
    now = now_utc or datetime.now(UTC)
    db_size_mb = (
        round(settings.db_path.stat().st_size / (1024**2), 2) if settings.db_path.exists() else 0.0
    )
    usage_target = settings.db_path.parent if settings.db_path.parent.exists() else Path.home()
    nvme_free_gb = round(shutil.disk_usage(usage_target).free / (1024**3), 2)

    total_papers = int(conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0])
    triaged_papers = int(
        conn.execute(
            "SELECT COUNT(DISTINCT arxiv_id) FROM triage_assessments WHERE rubric_id = 'ai_benchmark_triage'"
        ).fetchone()[0]
    )
    extracted_benchmarks = int(conn.execute("SELECT COUNT(*) FROM v_benchmarks").fetchone()[0])
    religion_papers = int(conn.execute("SELECT COUNT(*) FROM religious_bias_details").fetchone()[0])
    decision_scores = int(conn.execute("SELECT COUNT(*) FROM decision_scores").fetchone()[0])
    pending_uploads = int(
        conn.execute(
            "SELECT COUNT(*) FROM papers WHERE pdf_sync_status = 'pending_upload'"
        ).fetchone()[0]
    )
    quarantined = int(
        conn.execute(
            "SELECT COUNT(*) FROM paper_stage_status WHERE status = 'quarantined_invalid_schema'"
        ).fetchone()[0]
    )

    stage_counts: dict[str, dict[str, int]] = {}
    for row in conn.execute(
        "SELECT stage, status, COUNT(*) AS cnt FROM paper_stage_status GROUP BY stage, status"
    ).fetchall():
        stage_counts.setdefault(row["stage"], {})[row["status"]] = int(row["cnt"])

    watermarks: dict[str, dict[str, Any]] = {}
    alerts: list[str] = []
    latest_wm_age_hours: float | None = None

    for row in conn.execute("SELECT * FROM ingestion_checkpoints").fetchall():
        src = str(row["source"])
        updated_str = str(row["updated_at"])
        watermarks[src] = {
            "watermark_date": row["watermark_date"],
            "cursor_state": row["cursor_state"],
            "malformed_lines": int(row["malformed_lines"] or 0),
            "updated_at": updated_str,
        }
        try:
            dt = datetime.fromisoformat(updated_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            age_h = (now - dt).total_seconds() / 3600.0
            if latest_wm_age_hours is None or age_h < latest_wm_age_hours:
                latest_wm_age_hours = age_h
        except ValueError:
            pass
        if row["cursor_state"] == "incomplete_pagination":
            alerts.append(f"ALERT: Checkpoint '{src}' ended with incomplete_pagination.")

    if not watermarks:
        alerts.append("ALERT: No ingestion checkpoints recorded yet (run `arxiv-bench sync`).")
    elif latest_wm_age_hours is not None and latest_wm_age_hours > stale_hours:
        alerts.append(
            f"ALERT: Ingestion watermark is stale ({latest_wm_age_hours:.1f}h > {stale_hours:.0f}h threshold)."
        )

    if nvme_free_gb < 50.0:
        alerts.append(f"ALERT: Local NVMe free space low ({nvme_free_gb:.1f} GB < 50 GB).")

    if pending_uploads > 0:
        alerts.append(f"WARN: {pending_uploads} PDFs awaiting GCS archival retry (pending_upload).")

    local_latest = settings.db_path.parent / "backups" / "latest.db.zst"
    last_backup_at: str | None = None
    if local_latest.exists():
        mtime = datetime.fromtimestamp(local_latest.stat().st_mtime, tz=UTC)
        last_backup_at = mtime.isoformat()
        if (now - mtime).total_seconds() / 3600.0 > stale_hours:
            alerts.append("ALERT: Latest SQLite backup is older than 48 hours.")

    return StatusReport(
        db_path=str(settings.db_path),
        db_size_mb=db_size_mb,
        nvme_free_gb=nvme_free_gb,
        total_papers=total_papers,
        triaged_papers=triaged_papers,
        extracted_benchmarks=extracted_benchmarks,
        religion_papers=religion_papers,
        decision_score_rows=decision_scores,
        pending_pdf_uploads=pending_uploads,
        quarantined_papers=quarantined,
        stage_counts=stage_counts,
        watermarks=watermarks,
        last_backup_at=last_backup_at,
        alerts=alerts,
    )


def render_search_results(rows: list[dict[str, Any]], fmt: str = "table") -> str:
    """Format search results as table, csv, json, md, or bibtex."""
    if fmt == "json":
        return json.dumps(rows, indent=2)
    if fmt == "bibtex":
        return "\n\n".join(format_bibtex(r) for r in rows)
    if fmt == "csv":
        buf = io.StringIO()
        fields = [
            "arxiv_id",
            "published_date",
            "citation_count",
            "contribution_type",
            "venue",
            "title",
        ]
        w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
        return buf.getvalue()
    if fmt == "md":
        lines = ["| ArXiv ID | Date | Citations | Type | Title |", "|---|---|---|---|---|"]
        for r in rows:
            url = get_arxiv_url(r["arxiv_id"])
            title = str(r.get("title") or "").replace("|", "\\|")
            lines.append(
                f"| [{r['arxiv_id']}]({url}) | {r.get('published_date') or ''} | "
                f"{r.get('citation_count') if r.get('citation_count') is not None else ''} | "
                f"{r.get('contribution_type') or ''} | {title} |"
            )
        return "\n".join(lines)

    # Default compact text table
    lines = [f"{'ID':<14} {'DATE':<10} {'CITES':>6} {'TYPE':<16} TITLE"]
    lines.append("-" * 92)
    for r in rows:
        cites = "" if r.get("citation_count") is None else str(r["citation_count"])
        lines.append(
            f"{str(r['arxiv_id']):<14} {str(r.get('published_date') or ''):<10} "
            f"{cites:>6} {str(r.get('contribution_type') or ''):<16} "
            f"{str(r.get('title') or '')[:80]}"
        )
    return "\n".join(lines)


def render_matrix(matrix: CoverageMatrix, fmt: str = "table") -> str:
    """Format a CoverageMatrix as table, md, csv, or json."""
    if fmt == "json":
        return json.dumps(
            {
                "rows_dim": matrix.rows_dim,
                "cols_dim": matrix.cols_dim,
                "row_labels": matrix.row_labels,
                "col_labels": matrix.col_labels,
                "counts": {f"{r}|{c}": v for (r, c), v in matrix.counts.items()},
                "zero_cells": matrix.zero_cells,
            },
            indent=2,
        )
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow([f"{matrix.rows_dim}\\{matrix.cols_dim}", *matrix.col_labels])
        for rl in matrix.row_labels:
            w.writerow([rl, *[matrix.counts.get((rl, cl), 0) for cl in matrix.col_labels]])
        return buf.getvalue()
    if fmt == "md":
        header = (
            f"| {matrix.rows_dim} \\\\ {matrix.cols_dim} | " + " | ".join(matrix.col_labels) + " |"
        )
        sep = "|---|" + "|".join("---:" for _ in matrix.col_labels) + "|"
        lines = [header, sep]
        for rl in matrix.row_labels:
            vals = [str(matrix.counts.get((rl, cl), 0)) for cl in matrix.col_labels]
            lines.append(f"| {rl} | " + " | ".join(vals) + " |")
        return "\n".join(lines)

    col_w = max([12, *(len(c) for c in matrix.col_labels)])
    row_w = max([16, *(len(r) for r in matrix.row_labels)])
    header = f"{matrix.rows_dim:<{row_w}} " + " ".join(f"{c:>{col_w}}" for c in matrix.col_labels)
    lines = [header, "-" * len(header)]
    for rl in matrix.row_labels:
        vals = " ".join(f"{matrix.counts.get((rl, cl), 0):>{col_w}}" for cl in matrix.col_labels)
        lines.append(f"{rl:<{row_w}} {vals}")
    if matrix.zero_cells:
        lines.append(f"\nZero-count gap cells ({len(matrix.zero_cells)} total):")
        for rl, cl in matrix.zero_cells[:15]:
            lines.append(f"  - {rl} x {cl}")
    return "\n".join(lines)
