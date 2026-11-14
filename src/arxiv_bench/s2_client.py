"""Semantic Scholar Batch Graph API client for authoritative citations, venues, and references."""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import requests

from arxiv_bench.config import Settings, canonicalize_arxiv_id
from arxiv_bench.db import SingleWriterQueue

S2_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_FIELDS = (
    "paperId,externalIds,citationCount,influentialCitationCount,"
    "venue,references.paperId,references.title,references.externalIds"
)
MAX_BATCH_SIZE = 500


@dataclass
class S2EnrichStats:
    """Summary counts from a Semantic Scholar batch enrichment run."""

    requested: int = 0
    enriched: int = 0
    not_found: int = 0
    failed_batches: int = 0
    citations_linked: int = 0


class SemanticScholarClient:
    """Fetches canonical citations, venues, and reference graphs in 500-paper batches."""

    def __init__(
        self,
        settings: Settings,
        *,
        session: requests.Session | None = None,
        max_retries: int = 3,
        delay_seconds: float = 1.2,
    ) -> None:
        self._settings = settings
        self._http = session or requests.Session()
        self._max_retries = max_retries
        self._delay = delay_seconds

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "arxiv-bench/0.2",
        }
        if self._settings.s2_api_key:
            headers["x-api-key"] = self._settings.s2_api_key
        return headers

    def fetch_batch(
        self,
        arxiv_ids: list[str],
    ) -> tuple[list[dict[str, Any] | None] | None, str | None, int]:
        """POST up to 500 ARXIV:<id> identifiers; returns (records, error_msg, http_status)."""
        payload = {"ids": [f"ARXIV:{aid}" for aid in arxiv_ids]}
        last_err: str | None = None
        last_status = 500

        for attempt in range(self._max_retries):
            try:
                resp = self._http.post(
                    S2_BATCH_URL,
                    params={"fields": S2_FIELDS},
                    headers=self._headers(),
                    json=payload,
                    timeout=60,
                )
                last_status = resp.status_code
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        return data, None, 200
                    return None, "Unexpected non-list JSON response from S2 batch API", 200
                last_err = f"HTTP {resp.status_code}: {resp.text[:300]}"
                if (
                    resp.status_code in (429, 500, 502, 503, 504)
                    and attempt + 1 < self._max_retries
                ):
                    time.sleep(self._delay * (2**attempt))
                    continue
                return None, last_err, resp.status_code
            except requests.RequestException as exc:
                last_err = str(exc)[:300]
                if attempt + 1 < self._max_retries:
                    time.sleep(self._delay * (2**attempt))
                    continue
                return None, last_err, 503

        return None, last_err, last_status

    def enrich_papers(
        self,
        conn: sqlite3.Connection,
        writer: SingleWriterQueue,
        *,
        limit: int | None = None,
        stale_days: int = 30,
        run_id: str | None = None,
    ) -> S2EnrichStats:
        """Enrich extracted or religious-bias papers missing fresh Semantic Scholar metadata."""
        sql = """
            SELECT p.arxiv_id
            FROM papers p
            WHERE (p.extraction_json IS NOT NULL
                   OR EXISTS (SELECT 1 FROM religious_bias_details r WHERE r.arxiv_id = p.arxiv_id))
              AND (p.s2_fetched_at IS NULL
                   OR p.s2_last_error IS NOT NULL
                   OR julianday('now') - julianday(p.s2_fetched_at) >= ?)
            ORDER BY p.published_date DESC, p.arxiv_id DESC
        """
        params: list[Any] = [stale_days]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        ids = [str(r["arxiv_id"]) for r in conn.execute(sql, params).fetchall()]
        stats = S2EnrichStats(requested=len(ids))

        for idx in range(0, len(ids), MAX_BATCH_SIZE):
            if idx > 0 and self._delay > 0:
                time.sleep(self._delay)
            chunk = ids[idx : idx + MAX_BATCH_SIZE]
            t0 = time.monotonic()
            records, err, status = self.fetch_batch(chunk)
            latency_ms = int((time.monotonic() - t0) * 1000)
            now_iso = datetime.now(UTC).isoformat()

            writer.submit_sql(
                """
                INSERT INTO api_call_logs (
                    run_id, stage, endpoint, model, arxiv_id,
                    prompt_tokens, output_tokens, estimated_cost_usd,
                    latency_ms, http_status, created_at
                ) VALUES (?, 'enrich', 's2/paper/batch', 'semantic-scholar', ?, 0, 0, 0.0, ?, ?, ?)
                """,
                (run_id, f"batch:{len(chunk)}", latency_ms, status, now_iso),
            )

            if records is None:
                stats.failed_batches += 1
                # Explicitly preserve NULL citation_count (never write fake 0) and record s2_last_error
                for aid in chunk:
                    writer.submit_sql(
                        """
                        UPDATE papers
                        SET s2_last_error = ?,
                            s2_fetched_at = NULL
                        WHERE arxiv_id = ?
                        """,
                        (err or f"HTTP {status}", aid),
                    )
                continue

            for aid, rec in zip(chunk, records, strict=False):
                if rec is None:
                    stats.not_found += 1
                    writer.submit_sql(
                        """
                        UPDATE papers
                        SET s2_fetched_at = ?,
                            s2_last_error = NULL
                        WHERE arxiv_id = ?
                        """,
                        (now_iso, aid),
                    )
                    continue

                stats.enriched += 1
                s2_id = rec.get("paperId")
                cite_cnt = rec.get("citationCount")
                inf_cnt = rec.get("influentialCitationCount")
                venue = rec.get("venue") or None
                refs = rec.get("references") or []

                writer.submit_sql(
                    """
                    UPDATE papers
                    SET citation_count = ?,
                        influential_citation_count = ?,
                        venue = COALESCE(?, venue),
                        s2_paper_id = COALESCE(?, s2_paper_id),
                        s2_fetched_at = ?,
                        s2_last_error = NULL
                    WHERE arxiv_id = ?
                    """,
                    (cite_cnt, inf_cnt, venue, s2_id, now_iso, aid),
                )

                for ref in refs:
                    if not isinstance(ref, dict):
                        continue
                    ref_s2_id = ref.get("paperId")
                    if not ref_s2_id:
                        continue
                    ext_ids = ref.get("externalIds") or {}
                    raw_ref_arxiv = ext_ids.get("ArXiv") if isinstance(ext_ids, dict) else None
                    cited_arxiv = canonicalize_arxiv_id(raw_ref_arxiv)[0] if raw_ref_arxiv else None
                    cited_title = ref.get("title")
                    writer.submit_sql(
                        """
                        INSERT INTO paper_citations (citing_arxiv_id, cited_s2_id, cited_arxiv_id, cited_title)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(citing_arxiv_id, cited_s2_id) DO UPDATE SET
                            cited_arxiv_id = COALESCE(excluded.cited_arxiv_id, paper_citations.cited_arxiv_id),
                            cited_title = COALESCE(excluded.cited_title, paper_citations.cited_title)
                        """,
                        (aid, str(ref_s2_id), cited_arxiv, cited_title),
                    )
                    stats.citations_linked += 1

        writer.flush()
        return stats
