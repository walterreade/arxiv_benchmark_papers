"""Semantic Scholar Batch Graph API client for authoritative citations, venues, and references."""

from __future__ import annotations

import json
import logging
import random
import sqlite3
import sys
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
    elapsed_seconds: float = 0.0
    stopped_reason: str | None = None


class SemanticScholarClient:
    """Fetches canonical citations, venues, and reference graphs in 500-paper batches."""

    def __init__(
        self,
        settings: Settings,
        *,
        session: requests.Session | None = None,
        max_retries: int = 6,
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
                    retry_after = 0.0
                    raw_ra = getattr(resp, "headers", {}).get("Retry-After")
                    if raw_ra:
                        try:
                            retry_after = float(raw_ra)
                        except ValueError:
                            retry_after = 0.0
                    base_sleep = max(self._delay, 1.5) * (2**attempt)
                    sleep_for = min(45.0, max(retry_after, base_sleep)) + random.uniform(0.2, 1.0)
                    time.sleep(sleep_for)
                    continue
                return None, last_err, resp.status_code
            except requests.RequestException as exc:
                last_err = str(exc)[:300]
                if attempt + 1 < self._max_retries:
                    sleep_for = min(30.0, max(self._delay, 1.0) * (2**attempt))
                    time.sleep(sleep_for)
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
        progress_every_batches: int = 5,
        max_consecutive_failed_batches: int = 8,
        run_id: str | None = None,
    ) -> S2EnrichStats:
        """Enrich extracted or religious-bias papers missing fresh Semantic Scholar metadata."""
        logger = logging.getLogger("arxiv_bench")
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
        if not ids:
            return stats

        t_start = time.monotonic()
        total_batches = (len(ids) + MAX_BATCH_SIZE - 1) // MAX_BATCH_SIZE
        consecutive_failures = 0

        for batch_num, idx in enumerate(range(0, len(ids), MAX_BATCH_SIZE), start=1):
            if idx > 0 and self._delay > 0:
                time.sleep(self._delay)
            chunk = ids[idx : idx + MAX_BATCH_SIZE]
            t0 = time.monotonic()
            records, err, status = self.fetch_batch(chunk)
            latency_ms = int((time.monotonic() - t0) * 1000)
            now_iso = datetime.now(UTC).isoformat()

            if records is None:
                stats.failed_batches += 1
                consecutive_failures += 1
                err_text = err or f"HTTP {status}"
                err_rows = [(err_text, aid) for aid in chunk]

                def _write_failed_batch(
                    cur: sqlite3.Cursor,
                    _err_rows: list[tuple[str, str]] = err_rows,
                    _chunk_len: int = len(chunk),
                    _lat: int = latency_ms,
                    _status: int = status,
                    _now: str = now_iso,
                ) -> None:
                    cur.execute(
                        """
                        INSERT INTO api_call_logs (
                            run_id, stage, endpoint, model, arxiv_id,
                            prompt_tokens, output_tokens, estimated_cost_usd,
                            latency_ms, http_status, created_at
                        ) VALUES (?, 'enrich', 's2/paper/batch', 'semantic-scholar', ?, 0, 0, 0.0, ?, ?, ?)
                        """,
                        (run_id, f"batch:{_chunk_len}", _lat, _status, _now),
                    )
                    # Explicitly preserve NULL citation_count (never write fake 0)
                    cur.executemany(
                        """
                        UPDATE papers
                        SET s2_last_error = ?,
                            s2_fetched_at = NULL
                        WHERE arxiv_id = ?
                        """,
                        _err_rows,
                    )

                writer.submit(_write_failed_batch)
                writer.flush()
                if (
                    max_consecutive_failed_batches > 0
                    and consecutive_failures >= max_consecutive_failed_batches
                ):
                    stats.stopped_reason = "consecutive_failed_batches"
                    break
                continue

            consecutive_failures = 0
            not_found_rows: list[tuple[str, str]] = []
            enriched_rows: list[tuple[Any, ...]] = []
            citation_rows: list[tuple[str, str, str | None, str | None]] = []

            for aid, rec in zip(chunk, records, strict=False):
                if rec is None:
                    stats.not_found += 1
                    not_found_rows.append((now_iso, aid))
                    continue

                stats.enriched += 1
                s2_id = rec.get("paperId")
                cite_cnt = rec.get("citationCount")
                inf_cnt = rec.get("influentialCitationCount")
                venue = rec.get("venue") or None
                refs = rec.get("references") or []
                enriched_rows.append((cite_cnt, inf_cnt, venue, s2_id, now_iso, aid))

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
                    citation_rows.append((aid, str(ref_s2_id), cited_arxiv, cited_title))
                    stats.citations_linked += 1

            def _write_ok_batch(
                cur: sqlite3.Cursor,
                _not_found: list[tuple[str, str]] = not_found_rows,
                _enriched: list[tuple[Any, ...]] = enriched_rows,
                _citations: list[tuple[str, str, str | None, str | None]] = citation_rows,
                _chunk_len: int = len(chunk),
                _lat: int = latency_ms,
                _status: int = status,
                _now: str = now_iso,
            ) -> None:
                cur.execute(
                    """
                    INSERT INTO api_call_logs (
                        run_id, stage, endpoint, model, arxiv_id,
                        prompt_tokens, output_tokens, estimated_cost_usd,
                        latency_ms, http_status, created_at
                    ) VALUES (?, 'enrich', 's2/paper/batch', 'semantic-scholar', ?, 0, 0, 0.0, ?, ?, ?)
                    """,
                    (run_id, f"batch:{_chunk_len}", _lat, _status, _now),
                )
                if _not_found:
                    cur.executemany(
                        """
                        UPDATE papers
                        SET s2_fetched_at = ?,
                            s2_last_error = NULL
                        WHERE arxiv_id = ?
                        """,
                        _not_found,
                    )
                if _enriched:
                    cur.executemany(
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
                        _enriched,
                    )
                if _citations:
                    cur.executemany(
                        """
                        INSERT INTO paper_citations (citing_arxiv_id, cited_s2_id, cited_arxiv_id, cited_title)
                        VALUES (?, ?, ?, ?)
                        ON CONFLICT(citing_arxiv_id, cited_s2_id) DO UPDATE SET
                            cited_arxiv_id = COALESCE(excluded.cited_arxiv_id, paper_citations.cited_arxiv_id),
                            cited_title = COALESCE(excluded.cited_title, paper_citations.cited_title)
                        """,
                        _citations,
                    )

            writer.submit(_write_ok_batch)
            writer.flush()

            if progress_every_batches > 0 and (
                batch_num % progress_every_batches == 0 or batch_num == total_batches
            ):
                elapsed_s = max(1e-6, time.monotonic() - t_start)
                progress = {
                    "event": "enrich_progress",
                    "run_id": run_id,
                    "batch": batch_num,
                    "total_batches": total_batches,
                    "enriched": stats.enriched,
                    "not_found": stats.not_found,
                    "failed_batches": stats.failed_batches,
                    "citations_linked": stats.citations_linked,
                    "elapsed_s": round(elapsed_s, 1),
                }
                logger.info(json.dumps(progress))
                print(json.dumps(progress), file=sys.stderr, flush=True)

        writer.flush()
        stats.elapsed_seconds = round(time.monotonic() - t_start, 2)
        return stats
