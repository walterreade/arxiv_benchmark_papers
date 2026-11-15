"""Stage 2 unified interactive Gemini Flash PDF extraction workers and deterministic entity resolution."""

from __future__ import annotations

import json
import logging
import random
import sqlite3
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types
from pydantic import ValidationError

from arxiv_bench.config import ISO_DATE_GLOB, Settings
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.decision_client import (
    DailyQuotaExceededError,
    _extract_status_code,
    _is_retryable_network_error,
    is_daily_quota_error,
)
from arxiv_bench.flash_triage import flash_cost_rates_per_1m
from arxiv_bench.pdf_storage import (
    PdfStorageManager,
    WithdrawnPaperError,
    extract_local_text,
)
from arxiv_bench.schemas import (
    CONTROLLED_DOMAINS,
    CONTROLLED_MODALITIES,
    BenchmarkExtraction,
    normalize_domain,
    normalize_entity_slug,
    normalize_modality,
    normalize_repo_url,
)

INLINE_PDF_MAX_BYTES = 20 * 1024 * 1024  # 20 MB threshold
EXTRACTION_SCHEMA_VERSION = "v2.1"
FLASH_INPUT_COST_PER_1M = 0.30
FLASH_OUTPUT_COST_PER_1M = 2.50
DEFAULT_EXTRACT_TIMEOUT_MS = 180_000
DEFAULT_FILES_API_POLL_TIMEOUT_S = 120.0

STAGE2_EXTRACTION_PROMPT = f"""\
You are an expert AI evaluation researcher extracting structured metadata from an arXiv paper PDF.
Analyze ALL pages including tables, leaderboards, dataset split tables, appendices, and figures.

Rules:
1. Classify `contribution_type` accurately:
   - "introduces": creates a new benchmark, evaluation dataset, leaderboard, or evaluation framework.
   - "extends": translates, filters, hardens, scales, or adapts an existing benchmark.
   - "audits_critiques": analyzes benchmark flaws, saturation, contamination, annotator error, or validity.
   - "surveys": reviews or taxonomizes benchmarks, evaluation datasets, or evaluation methodologies.
   - "uses_only": proposes a model/method and only evaluates it on existing benchmarks.
   - "unrelated": not about AI/ML evaluation or benchmarks.
2. Extract exact benchmark names (preserving variant suffixes like "SWE-bench Verified" or "MMLU-Pro"),
   public repository/dataset URLs, tasks, evaluation methods, languages, models tested,
   base benchmarks referenced/extended, continuous testing status, and author-reported limitations.
3. For `modalities` and `domains`, choose ONLY 1-3 most applicable canonical tags from the fixed schema enums
   (modalities: {", ".join(CONTROLLED_MODALITIES)}; domains: {", ".join(CONTROLLED_DOMAINS)}).
   Put fine-grained sub-domains, sensor types, or problem specifics in `tasks` and `evidence_card`.
4. Produce a comprehensive `evidence_card` (~1,000-1,500 tokens total across its five fields) capturing
   task design, dataset construction, scoring protocol, contamination controls, and author-reported gaps.
5. Do NOT transcribe the paper's bibliography or reference list.
"""


@dataclass(frozen=True)
class DryRunEstimate:
    """Volume and spend preview returned by --dry-run."""

    pending_papers: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float
    estimated_minutes_at_50_rpm: float
    threshold: float = 0.50
    since: str | None = None
    until: str | None = None
    retry_failed: bool = False
    model: str = ""


@dataclass
class ExtractionStats:
    """Counters and telemetry for a Stage 2 extraction run."""

    attempted: int = 0
    succeeded: int = 0
    quarantined: int = 0
    withdrawn: int = 0
    failed: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    elapsed_seconds: float = 0.0
    observed_rpm: float = 0.0
    retries_429: int = 0
    retries_5xx: int = 0
    retries_network: int = 0
    sources: dict[str, int] = field(default_factory=dict)
    stopped_reason: str | None = None
    sample_errors: list[str] = field(default_factory=list)


class _RunStoppedSignal(Exception):
    """Internal sentinel raised when a shared stop_event halts in-flight workers cleanly."""


@dataclass
class _PaperOutcome:
    """Per-paper worker outcome aggregated by run_pending()."""

    status: str  # "succeeded", "quarantined", "withdrawn", "failed", "quota", "skipped"
    arxiv_id: str
    source: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    error_detail: str | None = None


def _build_pending_query_parts(
    *,
    threshold: float,
    since: str | None = None,
    until: str | None = None,
    retry_failed: bool = False,
) -> tuple[str, list[Any]]:
    """Return shared SQL FROM/WHERE fragment and params for Stage 2 pending selection."""
    status_clause = (
        "(s.status IS NULL OR s.status IN ('pending', 'failed') OR p.version_drift = 1)"
        if retry_failed
        else "(s.status IS NULL OR s.status = 'pending' OR p.version_drift = 1)"
    )
    where_parts = [
        "p.is_withdrawn = 0",
        status_clause,
        """NOT EXISTS (
            SELECT 1 FROM triage_assessments tc
            WHERE tc.arxiv_id = t.arxiv_id
              AND tc.paper_version = t.paper_version
              AND tc.rubric_id = t.rubric_id
              AND tc.rubric_version = t.rubric_version
              AND tc.question_id = 'contribution_type'
              AND tc.choice_or_bool IN ('uses_only', 'unrelated')
        )""",
    ]
    params: list[Any] = [threshold]
    if since or until:
        where_parts.append(f"p.published_date GLOB '{ISO_DATE_GLOB}'")
    if since:
        where_parts.append("p.published_date >= ?")
        params.append(since)
    if until:
        where_parts.append("p.published_date <= ?")
        params.append(until)

    from_where = f"""
        FROM papers p
        INNER JOIN triage_assessments t
            ON t.arxiv_id = p.arxiv_id
           AND t.rubric_id = 'ai_benchmark_triage'
           AND t.question_id = 'is_benchmark_contribution'
           AND t.probability >= ?
        LEFT JOIN paper_stage_status s
            ON s.arxiv_id = p.arxiv_id AND s.stage = 'extract'
        WHERE {" AND ".join(where_parts)}
    """
    return from_where, params


def resolve_and_upsert_entity(
    cur: sqlite3.Cursor,
    *,
    entity_type: str,
    raw_name: str,
    url: str | None = None,
    s2_id: str | None = None,
) -> str | None:
    """Deterministically resolve an entity via normalized URL, S2 ID, or variant-preserving slug."""
    cleaned_name = " ".join(raw_name.split())
    slug = normalize_entity_slug(cleaned_name)
    if not slug:
        return None
    norm_url = normalize_repo_url(url)

    # 1. Exact URL match
    if norm_url:
        row = cur.execute(
            "SELECT canonical_id FROM entities WHERE entity_type = ? AND canonical_url = ?",
            (entity_type, norm_url),
        ).fetchone()
        if row:
            canonical_id = str(row["canonical_id"])
            cur.execute(
                """
                INSERT OR IGNORE INTO entity_aliases (raw_slug, entity_type, canonical_id, resolution_method)
                VALUES (?, ?, ?, 'url_match')
                """,
                (slug, entity_type, canonical_id),
            )
            return canonical_id

    # 2. Exact Semantic Scholar paper ID match
    if s2_id:
        row = cur.execute(
            "SELECT canonical_id FROM entities WHERE entity_type = ? AND s2_paper_id = ?",
            (entity_type, s2_id),
        ).fetchone()
        if row:
            canonical_id = str(row["canonical_id"])
            cur.execute(
                """
                INSERT OR IGNORE INTO entity_aliases (raw_slug, entity_type, canonical_id, resolution_method)
                VALUES (?, ?, ?, 's2_id_match')
                """,
                (slug, entity_type, canonical_id),
            )
            return canonical_id

    # 3. Existing alias lookup by deterministic slug
    alias_row = cur.execute(
        "SELECT canonical_id FROM entity_aliases WHERE raw_slug = ? AND entity_type = ?",
        (slug, entity_type),
    ).fetchone()
    if alias_row:
        canonical_id = str(alias_row["canonical_id"])
        if norm_url or s2_id:
            cur.execute(
                """
                UPDATE entities
                SET canonical_url = COALESCE(canonical_url, ?),
                    s2_paper_id = COALESCE(s2_paper_id, ?)
                WHERE canonical_id = ?
                """,
                (norm_url, s2_id, canonical_id),
            )
        return canonical_id

    # 4. Create new canonical entity + alias
    canonical_id = f"{entity_type}:{slug}"
    cur.execute(
        """
        INSERT INTO entities (canonical_id, entity_type, canonical_name, canonical_url, s2_paper_id)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(canonical_id) DO UPDATE SET
            canonical_url = COALESCE(entities.canonical_url, excluded.canonical_url),
            s2_paper_id = COALESCE(entities.s2_paper_id, excluded.s2_paper_id)
        """,
        (canonical_id, entity_type, cleaned_name, norm_url, s2_id),
    )
    cur.execute(
        """
        INSERT OR IGNORE INTO entity_aliases (raw_slug, entity_type, canonical_id, resolution_method)
        VALUES (?, ?, ?, 'deterministic_slug')
        """,
        (slug, entity_type, canonical_id),
    )
    return canonical_id


def persist_extraction(
    cur: sqlite3.Cursor,
    *,
    arxiv_id: str,
    extracted_version: int,
    extraction: BenchmarkExtraction,
    page_count: int,
    chars_per_page: float,
    compressed_text_zst: bytes,
    gcs_pdf_uri: str | None,
    pdf_sha256: str,
    pdf_sync_status: str,
    run_id: str | None,
) -> None:
    """Write Stage 2 extraction payload, Evidence Card, compressed text, and normalized facets."""
    evidence_md = extraction.evidence_card.to_markdown()
    now_iso = datetime.now(UTC).isoformat()

    cur.execute(
        """
        UPDATE papers
        SET extracted_version = ?,
            version_drift = 0,
            page_count = ?,
            compressed_text_zst = ?,
            chars_per_page = ?,
            gcs_pdf_uri = COALESCE(?, gcs_pdf_uri),
            pdf_sha256 = ?,
            pdf_sync_status = ?,
            extraction_json = ?,
            evidence_card = ?,
            stated_limitations = ?,
            extraction_schema_version = ?
        WHERE arxiv_id = ?
        """,
        (
            extracted_version,
            page_count,
            compressed_text_zst,
            chars_per_page,
            gcs_pdf_uri,
            pdf_sha256,
            pdf_sync_status,
            extraction.model_dump_json(),
            evidence_md,
            extraction.stated_limitations,
            EXTRACTION_SCHEMA_VERSION,
            arxiv_id,
        ),
    )

    # Refresh normalized junction tables cleanly for idempotency on re-extraction
    for tbl in (
        "paper_benchmarks",
        "paper_modalities",
        "paper_domains",
        "paper_tasks",
        "paper_models",
    ):
        cur.execute(f"DELETE FROM {tbl} WHERE arxiv_id = ?", (arxiv_id,))

    for bench in extraction.benchmarks:
        cid = resolve_and_upsert_entity(
            cur,
            entity_type="benchmark",
            raw_name=bench.name,
            url=bench.url,
        )
        if cid:
            cur.execute(
                "INSERT OR IGNORE INTO paper_benchmarks (arxiv_id, canonical_id, role) VALUES (?, ?, ?)",
                (arxiv_id, cid, bench.role),
            )
        for base_name in bench.base_benchmarks:
            base_cid = resolve_and_upsert_entity(cur, entity_type="benchmark", raw_name=base_name)
            if base_cid:
                cur.execute(
                    "INSERT OR IGNORE INTO paper_benchmarks (arxiv_id, canonical_id, role) VALUES (?, ?, 'base_used')",
                    (arxiv_id, base_cid),
                )

    for base_name in extraction.base_benchmarks:
        base_cid = resolve_and_upsert_entity(cur, entity_type="benchmark", raw_name=base_name)
        if base_cid:
            cur.execute(
                "INSERT OR IGNORE INTO paper_benchmarks (arxiv_id, canonical_id, role) VALUES (?, ?, 'base_used')",
                (arxiv_id, base_cid),
            )

    for mod in extraction.modalities:
        norm = normalize_modality(mod)
        if norm:
            cur.execute(
                "INSERT OR IGNORE INTO paper_modalities (arxiv_id, modality) VALUES (?, ?)",
                (arxiv_id, norm),
            )
    for dom in extraction.domains:
        norm = normalize_domain(dom)
        if norm:
            cur.execute(
                "INSERT OR IGNORE INTO paper_domains (arxiv_id, domain) VALUES (?, ?)",
                (arxiv_id, norm),
            )
    for task in extraction.tasks:
        norm = normalize_entity_slug(task)
        if norm:
            cur.execute(
                "INSERT OR IGNORE INTO paper_tasks (arxiv_id, task) VALUES (?, ?)",
                (arxiv_id, norm),
            )
    for model_name in extraction.models_tested:
        m_cid = resolve_and_upsert_entity(cur, entity_type="model", raw_name=model_name)
        if m_cid:
            cur.execute(
                "INSERT OR IGNORE INTO paper_models (arxiv_id, canonical_id) VALUES (?, ?)",
                (arxiv_id, m_cid),
            )

    cur.execute(
        """
        INSERT INTO paper_stage_status (
            arxiv_id, stage, status, attempt_count, run_id, updated_at
        ) VALUES (?, 'extract', 'done', 1, ?, ?)
        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
            status = 'done',
            attempt_count = paper_stage_status.attempt_count + 1,
            last_error_code = NULL,
            last_error_detail = NULL,
            run_id = excluded.run_id,
            updated_at = excluded.updated_at
        """,
        (arxiv_id, run_id, now_iso),
    )


class ExtractionClient:
    """Unified interactive Gemini Flash inline-PDF extractor for backfill and daily runs."""

    def __init__(
        self,
        settings: Settings,
        storage: PdfStorageManager,
        *,
        client: Any | None = None,
        max_retries: int = 5,
        max_rpm: float | None = None,
        timeout_ms: int = DEFAULT_EXTRACT_TIMEOUT_MS,
        thinking_budget: int | None = None,
    ) -> None:
        self._settings = settings
        self._storage = storage
        self._client = client
        self._thread_local = threading.local()
        self._stats_lock = threading.Lock()
        self._pace_lock = threading.Lock()
        self._min_interval_s = (60.0 / max_rpm) if (max_rpm and max_rpm > 0) else 0.0
        self._next_allowed_at = 0.0
        self._cooldown_until = 0.0
        self._max_retries = max_retries
        self._timeout_ms = timeout_ms
        self._thinking_budget = thinking_budget
        self._disable_thinking_config = False
        self.retry_429_count = 0
        self.retry_5xx_count = 0
        self.retry_network_count = 0
        self.daily_quota_error: str | None = None

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        tls_client = getattr(self._thread_local, "client", None)
        if tls_client is None:
            if not self._settings.google_api_key:
                raise RuntimeError("GOOGLE_API_KEY is required for ExtractionClient.")
            tls_client = genai.Client(
                api_key=self._settings.google_api_key,
                http_options={"timeout": self._timeout_ms},
            )
            self._thread_local.client = tls_client
        return tls_client

    def _wait_for_slot(self, stop_event: threading.Event | None = None) -> bool:
        while True:
            if stop_event is not None and stop_event.is_set():
                return False
            with self._pace_lock:
                now = time.monotonic()
                wait_cd = self._cooldown_until - now
                if wait_cd > 0:
                    sleep_for = min(wait_cd, 2.0)
                    is_cd = True
                elif self._min_interval_s > 0:
                    target = max(now, self._next_allowed_at)
                    self._next_allowed_at = target + self._min_interval_s
                    sleep_for = target - now
                    is_cd = False
                else:
                    return True
            if sleep_for > 0:
                if stop_event is not None:
                    if stop_event.wait(timeout=sleep_for):
                        return False
                else:
                    time.sleep(sleep_for)
            if not is_cd:
                return True

    def sweep_orphan_files(self, *, max_age_hours: float = 2.0) -> int:
        """Delete stale Gemini Files API objects left behind by crashed >=20 MB uploads."""
        sdk = self._get_client()
        cutoff = datetime.now(UTC) - timedelta(hours=max_age_hours)
        deleted = 0
        try:
            for remote_file in sdk.files.list():
                create_time = getattr(remote_file, "create_time", None)
                if isinstance(create_time, datetime):
                    if create_time.tzinfo is None:
                        create_time = create_time.replace(tzinfo=UTC)
                    if create_time >= cutoff:
                        continue
                name = getattr(remote_file, "name", None)
                if name:
                    try:
                        sdk.files.delete(name=name)
                        deleted += 1
                    except Exception:  # noqa: BLE001
                        continue
        except Exception:  # noqa: BLE001
            return deleted
        return deleted

    def extract_from_pdf(
        self,
        pdf_path: Path,
        *,
        arxiv_id: str,
        title: str = "",
        writer: SingleWriterQueue | None = None,
        run_id: str | None = None,
        telemetry: dict[str, Any] | None = None,
        stop_event: threading.Event | None = None,
    ) -> tuple[BenchmarkExtraction | None, str | None]:
        """Run single-pass native multimodal Gemini Flash extraction on one staged PDF.

        Returns (BenchmarkExtraction, None) on success or (None, raw_response_or_error)
        when schema validation fails after retries (triggering quarantine).
        """
        sdk = self._get_client()
        size_bytes = pdf_path.stat().st_size
        prompt = f"{STAGE2_EXTRACTION_PROMPT}\nPaper Title: {title}\nArXiv ID: {arxiv_id}"
        last_raw: str | None = None
        in_rate, out_rate = flash_cost_rates_per_1m(self._settings.flash_model)

        for attempt in range(self._max_retries):
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)
            if not self._wait_for_slot(stop_event=stop_event):
                raise _RunStoppedSignal()
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)

            uploaded_file = None
            endpoint = (
                "generate_content_inline_pdf"
                if size_bytes < INLINE_PDF_MAX_BYTES
                else "generate_content_files_api"
            )
            t0 = time.monotonic()
            try:
                if size_bytes < INLINE_PDF_MAX_BYTES:
                    pdf_part = types.Part.from_bytes(
                        data=pdf_path.read_bytes(),
                        mime_type="application/pdf",
                    )
                    contents: list[Any] = [pdf_part, prompt]
                else:
                    uploaded_file = sdk.files.upload(file=str(pdf_path))
                    poll_deadline = time.monotonic() + DEFAULT_FILES_API_POLL_TIMEOUT_S
                    while (
                        getattr(getattr(uploaded_file, "state", None), "name", "") == "PROCESSING"
                    ):
                        if time.monotonic() >= poll_deadline:
                            raise TimeoutError(
                                f"Gemini Files API processing timed out for {arxiv_id}"
                            )
                        if stop_event is not None and stop_event.is_set():
                            raise _RunStoppedSignal()
                        time.sleep(1.0)
                        uploaded_file = sdk.files.get(name=uploaded_file.name)
                    if getattr(getattr(uploaded_file, "state", None), "name", "") == "FAILED":
                        raise RuntimeError(f"Gemini Files API failed processing {arxiv_id}")
                    contents = [uploaded_file, prompt]

                thinking_cfg = (
                    types.ThinkingConfig(thinking_budget=self._thinking_budget)
                    if (self._thinking_budget is not None and not self._disable_thinking_config)
                    else None
                )
                gen_cfg = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BenchmarkExtraction,
                    thinking_config=thinking_cfg,
                )
                try:
                    response = sdk.models.generate_content(
                        model=self._settings.flash_model,
                        contents=contents,
                        config=gen_cfg,
                    )
                except Exception as exc:  # noqa: BLE001
                    if thinking_cfg is not None and "thinking" in str(exc).lower():
                        self._disable_thinking_config = True
                        response = sdk.models.generate_content(
                            model=self._settings.flash_model,
                            contents=contents,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=BenchmarkExtraction,
                            ),
                        )
                    else:
                        raise
                latency_ms = int((time.monotonic() - t0) * 1000)
                usage = getattr(response, "usage_metadata", None)
                in_tok = int(getattr(usage, "prompt_token_count", 0) or 0)
                cand_tok = int(getattr(usage, "candidates_token_count", 0) or 0)
                thoughts_tok = int(getattr(usage, "thoughts_token_count", 0) or 0)
                out_tok = cand_tok + thoughts_tok
                cost = (in_tok / 1_000_000.0) * in_rate + (out_tok / 1_000_000.0) * out_rate

                if telemetry is not None:
                    telemetry["input_tokens"] = int(telemetry.get("input_tokens", 0)) + in_tok
                    telemetry["output_tokens"] = int(telemetry.get("output_tokens", 0)) + out_tok
                    telemetry["estimated_cost_usd"] = (
                        float(telemetry.get("estimated_cost_usd", 0.0)) + cost
                    )
                    telemetry["endpoint"] = endpoint
                    telemetry["latency_ms"] = latency_ms

                if writer is not None:
                    writer.submit_sql(
                        """
                        INSERT INTO api_call_logs (
                            run_id, stage, endpoint, model, arxiv_id,
                            prompt_tokens, output_tokens, estimated_cost_usd,
                            latency_ms, http_status, created_at
                        ) VALUES (?, 'extract', ?, ?, ?, ?, ?, ?, ?, 200, ?)
                        """,
                        (
                            run_id,
                            endpoint,
                            self._settings.flash_model,
                            arxiv_id,
                            in_tok,
                            out_tok,
                            cost,
                            latency_ms,
                            datetime.now(UTC).isoformat(),
                        ),
                    )

                raw_text = (getattr(response, "text", None) or "").strip()
                last_raw = raw_text
                parsed = BenchmarkExtraction.model_validate_json(raw_text)
                return parsed, None
            except _RunStoppedSignal:
                raise
            except (ValidationError, json.JSONDecodeError) as exc:
                last_raw = last_raw or str(exc)
                if attempt + 1 < self._max_retries:
                    if stop_event is not None:
                        if stop_event.wait(timeout=0.5 * (attempt + 1)):
                            raise _RunStoppedSignal() from None
                    else:
                        time.sleep(0.5 * (attempt + 1))
                    continue
                return None, last_raw[:4000]
            except Exception as exc:  # noqa: BLE001
                status = _extract_status_code(exc)
                latency_ms = int((time.monotonic() - t0) * 1000)
                if writer is not None:
                    writer.submit_sql(
                        """
                        INSERT INTO api_call_logs (
                            run_id, stage, endpoint, model, arxiv_id,
                            prompt_tokens, output_tokens, estimated_cost_usd,
                            latency_ms, http_status, created_at
                        ) VALUES (?, 'extract', ?, ?, ?, 0, 0, 0.0, ?, ?, ?)
                        """,
                        (
                            run_id,
                            endpoint,
                            self._settings.flash_model,
                            arxiv_id,
                            latency_ms,
                            status,
                            datetime.now(UTC).isoformat(),
                        ),
                    )
                if is_daily_quota_error(exc, status):
                    msg = str(exc)[:300]
                    with self._stats_lock:
                        self.daily_quota_error = msg
                    raise DailyQuotaExceededError(msg) from exc
                if _is_retryable_network_error(exc, status) and attempt + 1 < self._max_retries:
                    with self._stats_lock:
                        if status == 429:
                            self.retry_429_count += 1
                        elif status >= 500:
                            self.retry_5xx_count += 1
                        else:
                            self.retry_network_count += 1
                    if status == 429:
                        with self._pace_lock:
                            self._cooldown_until = max(self._cooldown_until, time.monotonic() + 2.5)
                    backoff = min(35.0, 2.0 * (2**attempt)) + random.uniform(0.3, 1.5)
                    if stop_event is not None:
                        if stop_event.wait(timeout=backoff):
                            raise _RunStoppedSignal() from None
                    else:
                        time.sleep(backoff)
                    continue
                raise
            finally:
                if uploaded_file is not None:
                    try:
                        sdk.files.delete(name=uploaded_file.name)
                    except Exception:  # noqa: BLE001
                        pass

        return None, last_raw

    def estimate_dry_run(
        self,
        conn: sqlite3.Connection,
        *,
        threshold: float = 0.50,
        since: str | None = None,
        until: str | None = None,
        retry_failed: bool = False,
        limit: int | None = None,
    ) -> DryRunEstimate:
        """Preview pending Stage 2 volume, tokens, and USD cost without API calls."""
        from_where, params = _build_pending_query_parts(
            threshold=threshold,
            since=since,
            until=until,
            retry_failed=retry_failed,
        )
        row = conn.execute(
            f"SELECT COUNT(DISTINCT p.arxiv_id) AS cnt {from_where}", params
        ).fetchone()
        pending = int(row["cnt"]) if row else 0
        if limit is not None:
            pending = min(pending, limit)
        # Observed Gemini Flash multimodal PDF averages (~13.5k input, ~1.1k output tokens)
        in_tok = pending * 13_500
        out_tok = pending * 1_100
        in_rate, out_rate = flash_cost_rates_per_1m(self._settings.flash_model)
        cost = (in_tok / 1_000_000.0) * in_rate + (out_tok / 1_000_000.0) * out_rate
        return DryRunEstimate(
            pending_papers=pending,
            estimated_input_tokens=in_tok,
            estimated_output_tokens=out_tok,
            estimated_cost_usd=round(cost, 2),
            estimated_minutes_at_50_rpm=round(pending / 50.0, 1),
            threshold=threshold,
            since=since,
            until=until,
            retry_failed=retry_failed,
            model=self._settings.flash_model,
        )

    def run_pending(
        self,
        conn: sqlite3.Connection,
        writer: SingleWriterQueue,
        *,
        threshold: float = 0.50,
        since: str | None = None,
        until: str | None = None,
        retry_failed: bool = False,
        limit: int | None = None,
        workers: int = 8,
        chunk_size: int = 250,
        max_cost_usd: float | None = None,
        progress_every: int = 50,
        max_consecutive_errors: int = 25,
        run_id: str | None = None,
    ) -> ExtractionStats:
        """Execute unified interactive inline PDF workers across pending qualifying papers."""
        logger = logging.getLogger("arxiv_bench")
        self.sweep_orphan_files()
        from_where, params = _build_pending_query_parts(
            threshold=threshold,
            since=since,
            until=until,
            retry_failed=retry_failed,
        )
        sql = f"""
            SELECT DISTINCT p.arxiv_id, p.title, p.published_date, p.latest_version_seen, p.gcs_pdf_uri
            {from_where}
            ORDER BY
                CASE WHEN p.published_date GLOB '{ISO_DATE_GLOB}' THEN p.published_date ELSE '' END DESC,
                p.arxiv_id DESC
        """
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        rows = conn.execute(sql, params).fetchall()
        stats = ExtractionStats()
        total_planned = len(rows)
        if not rows:
            return stats

        t_start = time.monotonic()
        stop_event = threading.Event()
        effective_chunk = max(1, chunk_size)
        consecutive_errors = 0
        last_progress_at = 0

        def _emit_progress() -> None:
            elapsed_s = max(1e-6, time.monotonic() - t_start)
            rpm = stats.succeeded / (elapsed_s / 60.0)
            payload = {
                "event": "extract_progress",
                "run_id": run_id,
                "attempted": stats.attempted,
                "total_planned": total_planned,
                "succeeded": stats.succeeded,
                "quarantined": stats.quarantined,
                "withdrawn": stats.withdrawn,
                "failed": stats.failed,
                "retries_429": self.retry_429_count,
                "retries_5xx": self.retry_5xx_count,
                "retries_network": self.retry_network_count,
                "elapsed_s": round(elapsed_s, 1),
                "rpm": round(rpm, 1),
                "est_cost_usd": round(stats.estimated_cost_usd, 4),
                "sources": dict(stats.sources),
            }
            logger.info(json.dumps(payload))
            print(json.dumps(payload), file=sys.stderr, flush=True)

        def _process_one(row: sqlite3.Row) -> _PaperOutcome:
            arxiv_id = str(row["arxiv_id"])
            if stop_event.is_set() or self.daily_quota_error is not None:
                return _PaperOutcome(status="skipped", arxiv_id=arxiv_id)

            title = str(row["title"] or "")
            pub_date = row["published_date"]
            ver = int(row["latest_version_seen"] or 1)
            staged = None
            source_name: str | None = None
            telemetry: dict[str, Any] = {}
            try:
                staged = self._storage.stage_pdf(
                    arxiv_id,
                    gcs_pdf_uri=row["gcs_pdf_uri"],
                    version=ver,
                )
                source_name = staged.source
                if stop_event.is_set() or self.daily_quota_error is not None:
                    return _PaperOutcome(status="skipped", arxiv_id=arxiv_id, source=source_name)

                local_text = extract_local_text(staged.local_path)
                extraction, raw_err = self.extract_from_pdf(
                    staged.local_path,
                    arxiv_id=arxiv_id,
                    title=title,
                    writer=writer,
                    run_id=run_id,
                    telemetry=telemetry,
                    stop_event=stop_event,
                )
                archive = self._storage.archive_and_cleanup(staged, published_date=pub_date)
                staged = None  # already cleaned up by archive_and_cleanup

                in_tok = int(telemetry.get("input_tokens", 0))
                out_tok = int(telemetry.get("output_tokens", 0))
                cost_usd = float(telemetry.get("estimated_cost_usd", 0.0))

                if extraction is None:
                    now_iso = datetime.now(UTC).isoformat()
                    writer.submit_sql(
                        """
                        INSERT INTO paper_stage_status (
                            arxiv_id, stage, status, attempt_count,
                            last_error_code, last_error_detail, run_id, updated_at
                        ) VALUES (?, 'extract', 'quarantined_invalid_schema', 1, 'INVALID_SCHEMA', ?, ?, ?)
                        ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                            status = 'quarantined_invalid_schema',
                            attempt_count = paper_stage_status.attempt_count + 1,
                            last_error_code = 'INVALID_SCHEMA',
                            last_error_detail = excluded.last_error_detail,
                            run_id = excluded.run_id,
                            updated_at = excluded.updated_at
                        """,
                        (arxiv_id, raw_err, run_id, now_iso),
                    )
                    return _PaperOutcome(
                        status="quarantined",
                        arxiv_id=arxiv_id,
                        source=source_name,
                        input_tokens=in_tok,
                        output_tokens=out_tok,
                        estimated_cost_usd=cost_usd,
                    )

                writer.submit(
                    lambda cur: persist_extraction(
                        cur,
                        arxiv_id=arxiv_id,
                        extracted_version=ver,
                        extraction=extraction,
                        page_count=local_text.page_count,
                        chars_per_page=local_text.chars_per_page,
                        compressed_text_zst=local_text.compressed_zst,
                        gcs_pdf_uri=archive.gcs_pdf_uri,
                        pdf_sha256=archive.pdf_sha256,
                        pdf_sync_status=archive.pdf_sync_status,
                        run_id=run_id,
                    )
                )
                return _PaperOutcome(
                    status="succeeded",
                    arxiv_id=arxiv_id,
                    source=source_name,
                    input_tokens=in_tok,
                    output_tokens=out_tok,
                    estimated_cost_usd=cost_usd,
                )
            except _RunStoppedSignal:
                return _PaperOutcome(
                    status="skipped",
                    arxiv_id=arxiv_id,
                    source=source_name,
                    input_tokens=int(telemetry.get("input_tokens", 0)),
                    output_tokens=int(telemetry.get("output_tokens", 0)),
                    estimated_cost_usd=float(telemetry.get("estimated_cost_usd", 0.0)),
                )
            except DailyQuotaExceededError as exc:
                stop_event.set()
                return _PaperOutcome(
                    status="quota",
                    arxiv_id=arxiv_id,
                    source=source_name,
                    input_tokens=int(telemetry.get("input_tokens", 0)),
                    output_tokens=int(telemetry.get("output_tokens", 0)),
                    estimated_cost_usd=float(telemetry.get("estimated_cost_usd", 0.0)),
                    error_detail=f"{arxiv_id}: DailyQuotaExceededError: {str(exc)[:300]}",
                )
            except WithdrawnPaperError as exc:
                now_iso = datetime.now(UTC).isoformat()
                writer.submit_sql(
                    "UPDATE papers SET is_withdrawn = 1 WHERE arxiv_id = ?", (arxiv_id,)
                )
                writer.submit_sql(
                    """
                    INSERT INTO paper_stage_status (
                        arxiv_id, stage, status, attempt_count,
                        last_error_code, last_error_detail, run_id, updated_at
                    ) VALUES (?, 'extract', 'withdrawn', 1, 'WITHDRAWN', ?, ?, ?)
                    ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                        status = 'withdrawn',
                        last_error_detail = excluded.last_error_detail,
                        updated_at = excluded.updated_at
                    """,
                    (arxiv_id, str(exc)[:500], run_id, now_iso),
                )
                return _PaperOutcome(
                    status="withdrawn",
                    arxiv_id=arxiv_id,
                    source=source_name,
                )
            except Exception as exc:  # noqa: BLE001
                now_iso = datetime.now(UTC).isoformat()
                http_status = _extract_status_code(exc)
                err_code = f"API_{http_status}" if http_status > 0 else type(exc).__name__[:40]
                err_detail = f"{type(exc).__name__}: {str(exc)[:900]}"
                writer.submit_sql(
                    """
                    INSERT INTO paper_stage_status (
                        arxiv_id, stage, status, attempt_count,
                        last_error_code, last_error_detail, run_id, updated_at
                    ) VALUES (?, 'extract', 'failed', 1, ?, ?, ?, ?)
                    ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                        status = 'failed',
                        attempt_count = paper_stage_status.attempt_count + 1,
                        last_error_code = excluded.last_error_code,
                        last_error_detail = excluded.last_error_detail,
                        run_id = excluded.run_id,
                        updated_at = excluded.updated_at
                    """,
                    (arxiv_id, err_code, err_detail, run_id, now_iso),
                )
                return _PaperOutcome(
                    status="failed",
                    arxiv_id=arxiv_id,
                    source=source_name,
                    input_tokens=int(telemetry.get("input_tokens", 0)),
                    output_tokens=int(telemetry.get("output_tokens", 0)),
                    estimated_cost_usd=float(telemetry.get("estimated_cost_usd", 0.0)),
                    error_detail=f"{arxiv_id}: {err_detail[:300]}",
                )
            finally:
                if staged is not None:
                    self._storage.cleanup_staged(staged)

        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            for chunk_start in range(0, total_planned, effective_chunk):
                if stop_event.is_set():
                    break
                chunk = rows[chunk_start : chunk_start + effective_chunk]
                futs = [pool.submit(_process_one, r) for r in chunk]
                for fut in as_completed(futs):
                    if fut.cancelled():
                        continue
                    outcome = fut.result()
                    stats.total_input_tokens += outcome.input_tokens
                    stats.total_output_tokens += outcome.output_tokens
                    stats.estimated_cost_usd += outcome.estimated_cost_usd
                    if outcome.status == "skipped":
                        continue
                    if outcome.status == "quota":
                        if (
                            outcome.error_detail
                            and len(stats.sample_errors) < 10
                            and outcome.error_detail not in stats.sample_errors
                        ):
                            stats.sample_errors.append(outcome.error_detail)
                        if stats.stopped_reason is None:
                            stats.stopped_reason = "daily_quota_exceeded"
                        stop_event.set()
                        for pending_f in futs:
                            pending_f.cancel()
                        continue

                    stats.attempted += 1
                    if outcome.source:
                        stats.sources[outcome.source] = stats.sources.get(outcome.source, 0) + 1

                    if outcome.status == "succeeded":
                        stats.succeeded += 1
                        consecutive_errors = 0
                    elif outcome.status == "quarantined":
                        stats.quarantined += 1
                        consecutive_errors = 0
                    elif outcome.status == "withdrawn":
                        stats.withdrawn += 1
                        consecutive_errors = 0
                    else:
                        stats.failed += 1
                        consecutive_errors += 1
                        if (
                            outcome.error_detail
                            and len(stats.sample_errors) < 10
                            and outcome.error_detail not in stats.sample_errors
                        ):
                            stats.sample_errors.append(outcome.error_detail)

                    if stats.stopped_reason is None:
                        if max_cost_usd is not None and stats.estimated_cost_usd >= max_cost_usd:
                            stats.stopped_reason = "max_cost_usd_reached"
                            stop_event.set()
                        elif (
                            max_consecutive_errors > 0
                            and consecutive_errors >= max_consecutive_errors
                        ):
                            stats.stopped_reason = "consecutive_errors_guard"
                            stop_event.set()
                        elif stats.attempted >= 100 and (stats.failed / stats.attempted) > 0.15:
                            stats.stopped_reason = "failure_rate_exceeded_15pct"
                            stop_event.set()
                        if stop_event.is_set():
                            for pending_f in futs:
                                pending_f.cancel()

                    if (
                        progress_every > 0
                        and stats.attempted > 0
                        and (stats.attempted - last_progress_at) >= progress_every
                    ):
                        _emit_progress()
                        last_progress_at = stats.attempted

                writer.flush()
                if stats.attempted > last_progress_at and progress_every > 0:
                    _emit_progress()
                    last_progress_at = stats.attempted
                if stop_event.is_set():
                    break

        elapsed_s = max(1e-6, time.monotonic() - t_start)
        stats.estimated_cost_usd = round(stats.estimated_cost_usd, 6)
        stats.elapsed_seconds = round(elapsed_s, 2)
        stats.observed_rpm = round(stats.succeeded / (elapsed_s / 60.0), 2)
        stats.retries_429 = self.retry_429_count
        stats.retries_5xx = self.retry_5xx_count
        stats.retries_network = self.retry_network_count
        return stats
