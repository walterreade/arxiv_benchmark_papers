"""Gemini Flash batched Stage 1 triage fallback used when Decisions daily quota is exhausted."""

from __future__ import annotations

import json
import random
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

import requests
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel, Field

from arxiv_bench.config import Settings, canonicalize_arxiv_id
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.decision_client import (
    DailyQuotaExceededError,
    PermanentDecisionError,
    _extract_status_code,
    _is_retryable_network_error,
    _normalize_model_name,
    classify_decision_error,
    is_daily_quota_error,
)
from arxiv_bench.schemas import RubricPack

FLASH_TRIAGE_INPUT_COST_PER_1M_USD = 0.30
FLASH_TRIAGE_OUTPUT_COST_PER_1M_USD = 2.50
FLASH_LITE_INPUT_COST_PER_1M_USD = 0.10
FLASH_LITE_OUTPUT_COST_PER_1M_USD = 0.40
DEFAULT_FLASH_TRIAGE_TIMEOUT_MS = 120_000


def flash_cost_rates_per_1m(model_name: str) -> tuple[float, float]:
    """Return conservative (input_usd_per_1m, output_usd_per_1m) rates for a Flash model."""
    if "flash-lite" in model_name.lower():
        return FLASH_LITE_INPUT_COST_PER_1M_USD, FLASH_LITE_OUTPUT_COST_PER_1M_USD
    return FLASH_TRIAGE_INPUT_COST_PER_1M_USD, FLASH_TRIAGE_OUTPUT_COST_PER_1M_USD


ContributionTypeLiteral = Literal[
    "introduces",
    "extends",
    "audits_critiques",
    "surveys",
    "uses_only",
    "unrelated",
]
PrimaryModalityLiteral = Literal[
    "text_llm",
    "vision",
    "audio_speech",
    "video",
    "multimodal",
    "agent_tool_use",
    "robotics_embodied",
    "code_software",
    "tabular_timeseries",
    "scientific_medical",
    "other_emergent",
]


class FlashPaperTriageItem(BaseModel):
    """Single paper classification returned inside a batched Flash triage response."""

    arxiv_id: str
    is_benchmark_prob: float = Field(ge=0.0, le=1.0)
    contribution_type: ContributionTypeLiteral
    primary_modality: PrimaryModalityLiteral
    is_bias_religion_prob: float = Field(ge=0.0, le=1.0)


class FlashBatchTriageResponse(BaseModel):
    """Structured JSON schema for batched Stage 1 Flash abstract triage."""

    items: list[FlashPaperTriageItem]


@dataclass(frozen=True)
class TriagePaperInput:
    """Minimal paper payload required for Stage 1 abstract triage."""

    arxiv_id: str
    paper_version: int
    title: str
    abstract: str
    categories: list[str]


@dataclass
class FlashBatchResult:
    """Outcome summary for a single batched Gemini Flash triage call."""

    succeeded_ids: list[str] = field(default_factory=list)
    missing_ids: list[str] = field(default_factory=list)
    permanent_failed: dict[str, tuple[int, str]] = field(default_factory=dict)
    transient_failed: dict[str, tuple[int, str]] = field(default_factory=dict)
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    latency_ms: int = 0


def _build_rubric_prompt_section(rubric_pack: RubricPack) -> str:
    lines: list[str] = []
    for q in rubric_pack.questions:
        lines.append(f"### {q.id}\n{q.instructions.strip()}")
        if q.true_description:
            lines.append(f"- TRUE: {q.true_description.strip()}")
        if q.false_description:
            lines.append(f"- FALSE: {q.false_description.strip()}")
        if q.choices:
            for choice_key, choice_desc in q.choices.items():
                lines.append(f"- {choice_key}: {choice_desc.strip()}")
    return "\n".join(lines)


def _build_batch_prompt(papers: list[TriagePaperInput], rubric_pack: RubricPack) -> str:
    rubric_text = _build_rubric_prompt_section(rubric_pack)
    paper_blocks: list[str] = []
    for p in papers:
        cats = " ".join(p.categories)
        paper_blocks.append(
            f"[PAPER arxiv_id={p.arxiv_id}]\n"
            f"Title: {p.title}\n"
            f"Categories: {cats}\n"
            f"Abstract: {p.abstract}"
        )
    return (
        "You are performing Stage 1 AI benchmark triage on arXiv papers.\n"
        "Classify EVERY paper below according to the rubric.\n"
        "Output rules:\n"
        "- Return exactly one object in `items` for every input paper, preserving `arxiv_id` verbatim.\n"
        "- `is_benchmark_prob`: calibrated probability in [0.0, 1.0] for `is_benchmark_contribution`.\n"
        "- `contribution_type`: best matching choice for `contribution_type`.\n"
        "- `primary_modality`: best matching choice for `primary_modality`.\n"
        "- `is_bias_religion_prob`: calibrated probability in [0.0, 1.0] for `is_llm_bias_ethics_religion`.\n\n"
        f"{rubric_text}\n\n"
        "PAPERS:\n" + "\n\n".join(paper_blocks)
    )


class FlashTriageClient:
    """Thread-safe Gemini Flash batched Stage 1 triage client for Decisions quota fallback."""

    def __init__(
        self,
        settings: Settings,
        *,
        model: str | None = None,
        client: Any | None = None,
        max_retries: int = 6,
        max_rpm: float | None = None,
        stage: str = "triage_flash",
    ) -> None:
        self._settings = settings
        self._model = model or settings.flash_model
        self._stage = stage
        self._client = client
        self._thread_local = threading.local()
        self._stats_lock = threading.Lock()
        self._pace_lock = threading.Lock()
        self._min_interval_s = (60.0 / max_rpm) if (max_rpm and max_rpm > 0) else 0.0
        self._next_allowed_at = 0.0
        self._cooldown_until = 0.0
        self._max_retries = max_retries
        self._disable_thinking_budget = False
        self.retry_429_count = 0
        self.retry_5xx_count = 0
        self.retry_network_count = 0
        self.daily_quota_error: str | None = None

    @property
    def model_name(self) -> str:
        return _normalize_model_name(self._model)

    def _get_sdk_client(self) -> Any:
        if self._client is not None:
            return self._client
        tls_client = getattr(self._thread_local, "client", None)
        if tls_client is None:
            if not self._settings.google_api_key:
                raise RuntimeError("GOOGLE_API_KEY is required for FlashTriageClient.")
            tls_client = genai.Client(
                api_key=self._settings.google_api_key,
                http_options={"timeout": DEFAULT_FLASH_TRIAGE_TIMEOUT_MS},
            )
            self._thread_local.client = tls_client
        return tls_client

    def _wait_for_slot(self) -> None:
        while True:
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
                    return
            if sleep_for > 0:
                time.sleep(sleep_for)
            if not is_cd:
                return

    def _invoke_flash(self, prompt: str) -> tuple[FlashBatchTriageResponse, int, int, int]:
        sdk = self._get_sdk_client()
        thinking_cfg = (
            None if self._disable_thinking_budget else types.ThinkingConfig(thinking_budget=0)
        )
        cfg = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=FlashBatchTriageResponse,
            temperature=0.0,
            thinking_config=thinking_cfg,
        )
        try:
            resp = sdk.models.generate_content(
                model=self._model,
                contents=prompt,
                config=cfg,
            )
        except Exception as exc:  # noqa: BLE001
            # Some Flash-Lite variants reject thinking_budget=0; transparently retry without it once.
            if not self._disable_thinking_budget and "thinking" in str(exc).lower():
                self._disable_thinking_budget = True
                cfg_fallback = types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=FlashBatchTriageResponse,
                    temperature=0.0,
                )
                resp = sdk.models.generate_content(
                    model=self._model,
                    contents=prompt,
                    config=cfg_fallback,
                )
            else:
                raise

        raw_text = (getattr(resp, "text", None) or "").strip()
        if not raw_text:
            raise PermanentDecisionError(
                "Empty response returned by Flash triage (possible safety filter)",
                status_code=422,
            )
        parsed = FlashBatchTriageResponse.model_validate_json(raw_text)
        usage = getattr(resp, "usage_metadata", None)
        in_tok = int(getattr(usage, "prompt_token_count", 0) or 0)
        out_tok = int(getattr(usage, "candidates_token_count", 0) or 0)
        thoughts_tok = int(getattr(usage, "thoughts_token_count", 0) or 0)
        return parsed, in_tok, out_tok + thoughts_tok, 200

    def _call_with_retries(
        self,
        *,
        prompt: str,
        arxiv_id_label: str,
        run_id: str | None,
        writer: SingleWriterQueue | None,
    ) -> tuple[FlashBatchTriageResponse, int, int, float, int]:
        model_id = self.model_name
        last_exc: BaseException | None = None
        for attempt in range(self._max_retries):
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)
            self._wait_for_slot()
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)
            t0 = time.monotonic()
            try:
                parsed, in_tok, out_tok, http_status = self._invoke_flash(prompt)
                latency_ms = int((time.monotonic() - t0) * 1000)
                if in_tok <= 0:
                    in_tok = max(1, len(prompt) // 4)
                in_rate, out_rate = flash_cost_rates_per_1m(model_id)
                cost_usd = (in_tok / 1_000_000.0) * in_rate + (out_tok / 1_000_000.0) * out_rate
                if writer is not None:
                    writer.submit_sql(
                        """
                        INSERT INTO api_call_logs (
                            run_id, stage, endpoint, model, arxiv_id,
                            prompt_tokens, output_tokens, estimated_cost_usd,
                            latency_ms, http_status, created_at
                        ) VALUES (?, ?, 'generateContent', ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            run_id,
                            self._stage,
                            model_id,
                            arxiv_id_label,
                            in_tok,
                            out_tok,
                            cost_usd,
                            latency_ms,
                            http_status,
                            datetime.now(UTC).isoformat(),
                        ),
                    )
                return parsed, in_tok, out_tok, cost_usd, latency_ms
            except (
                genai_errors.APIError,
                requests.RequestException,
                RuntimeError,
                Exception,
            ) as exc:
                last_exc = exc
                status = _extract_status_code(exc)
                latency_ms = int((time.monotonic() - t0) * 1000)
                if writer is not None:
                    writer.submit_sql(
                        """
                        INSERT INTO api_call_logs (
                            run_id, stage, endpoint, model, arxiv_id,
                            prompt_tokens, output_tokens, estimated_cost_usd,
                            latency_ms, http_status, created_at
                        ) VALUES (?, ?, 'generateContent', ?, ?, 0, 0, 0.0, ?, ?, ?)
                        """,
                        (
                            run_id,
                            self._stage,
                            model_id,
                            arxiv_id_label,
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
                    backoff = min(35.0, (2.5 * (2**attempt))) + random.uniform(0.5, 2.5)
                    time.sleep(backoff)
                    continue
                raise

        assert last_exc is not None
        raise last_exc

    def _persist_items(
        self,
        *,
        matched: list[tuple[TriagePaperInput, FlashPaperTriageItem]],
        rubric_pack: RubricPack,
        writer: SingleWriterQueue,
        run_id: str | None,
    ) -> None:
        if not matched:
            return
        now_iso = datetime.now(UTC).isoformat()
        model_id = self.model_name
        assessment_rows: list[tuple[Any, ...]] = []
        status_rows: list[tuple[Any, ...]] = []

        for paper, item in matched:
            p_bench = round(max(0.0, min(1.0, float(item.is_benchmark_prob))), 6)
            p_rel = round(max(0.0, min(1.0, float(item.is_bias_religion_prob))), 6)
            assessment_rows.extend(
                [
                    (
                        paper.arxiv_id,
                        paper.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                        "is_benchmark_contribution",
                        model_id,
                        "true" if p_bench >= 0.5 else "false",
                        p_bench,
                        json.dumps({"true": p_bench, "false": round(1.0 - p_bench, 6)}),
                        now_iso,
                    ),
                    (
                        paper.arxiv_id,
                        paper.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                        "contribution_type",
                        model_id,
                        item.contribution_type,
                        1.0,
                        json.dumps({item.contribution_type: 1.0}),
                        now_iso,
                    ),
                    (
                        paper.arxiv_id,
                        paper.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                        "primary_modality",
                        model_id,
                        item.primary_modality,
                        1.0,
                        json.dumps({item.primary_modality: 1.0}),
                        now_iso,
                    ),
                    (
                        paper.arxiv_id,
                        paper.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                        "is_llm_bias_ethics_religion",
                        model_id,
                        "true" if p_rel >= 0.5 else "false",
                        p_rel,
                        json.dumps({"true": p_rel, "false": round(1.0 - p_rel, 6)}),
                        now_iso,
                    ),
                ]
            )
            status_rows.append((paper.arxiv_id, run_id, now_iso))

        def _write_batch(cur: sqlite3.Cursor) -> None:
            cur.executemany(
                """
                INSERT INTO triage_assessments (
                    arxiv_id, paper_version, rubric_id, rubric_version,
                    question_id, model_id, choice_or_bool, probability,
                    distribution_json, assessed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(arxiv_id, paper_version, rubric_id, rubric_version, question_id)
                DO UPDATE SET
                    model_id = excluded.model_id,
                    choice_or_bool = excluded.choice_or_bool,
                    probability = excluded.probability,
                    distribution_json = excluded.distribution_json,
                    assessed_at = excluded.assessed_at
                """,
                assessment_rows,
            )
            cur.executemany(
                """
                INSERT INTO paper_stage_status (
                    arxiv_id, stage, status, attempt_count, run_id, updated_at
                ) VALUES (?, 'triage', 'done', 1, ?, ?)
                ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                    status = 'done',
                    attempt_count = paper_stage_status.attempt_count + 1,
                    last_error_code = NULL,
                    last_error_detail = NULL,
                    run_id = excluded.run_id,
                    updated_at = excluded.updated_at
                """,
                status_rows,
            )

        writer.submit(_write_batch)

    def score_abstract_batch(
        self,
        *,
        papers: list[TriagePaperInput],
        rubric_pack: RubricPack,
        writer: SingleWriterQueue | None = None,
        run_id: str | None = None,
        allow_bisect: bool = True,
    ) -> FlashBatchResult:
        """Score a batch of abstracts via Gemini Flash, isolating poison rows via single-item fallback."""
        result = FlashBatchResult()
        if not papers:
            return result

        prompt = _build_batch_prompt(papers, rubric_pack)
        label = (
            papers[0].arxiv_id if len(papers) == 1 else f"batch:{len(papers)}:{papers[0].arxiv_id}"
        )
        try:
            parsed, in_tok, out_tok, cost_usd, latency_ms = self._call_with_retries(
                prompt=prompt,
                arxiv_id_label=label,
                run_id=run_id,
                writer=writer,
            )
        except DailyQuotaExceededError:
            raise
        except Exception as exc:  # noqa: BLE001
            is_perm, err_code, err_detail = classify_decision_error(exc)
            # If a multi-paper batch failed with a permanent/schema error, bisect to isolate any bad abstract.
            if allow_bisect and len(papers) > 1 and (is_perm or "validation" in err_detail.lower()):
                mid = len(papers) // 2
                left = self.score_abstract_batch(
                    papers=papers[:mid],
                    rubric_pack=rubric_pack,
                    writer=writer,
                    run_id=run_id,
                    allow_bisect=True,
                )
                right = self.score_abstract_batch(
                    papers=papers[mid:],
                    rubric_pack=rubric_pack,
                    writer=writer,
                    run_id=run_id,
                    allow_bisect=True,
                )
                result.succeeded_ids.extend(left.succeeded_ids + right.succeeded_ids)
                result.missing_ids.extend(left.missing_ids + right.missing_ids)
                result.permanent_failed.update(left.permanent_failed)
                result.permanent_failed.update(right.permanent_failed)
                result.transient_failed.update(left.transient_failed)
                result.transient_failed.update(right.transient_failed)
                result.input_tokens = left.input_tokens + right.input_tokens
                result.output_tokens = left.output_tokens + right.output_tokens
                result.estimated_cost_usd = left.estimated_cost_usd + right.estimated_cost_usd
                result.latency_ms = left.latency_ms + right.latency_ms
                return result

            for p in papers:
                if is_perm:
                    result.permanent_failed[p.arxiv_id] = (err_code, err_detail)
                else:
                    result.transient_failed[p.arxiv_id] = (err_code, err_detail)
            return result

        result.input_tokens += in_tok
        result.output_tokens += out_tok
        result.estimated_cost_usd += cost_usd
        result.latency_ms += latency_ms

        by_id: dict[str, FlashPaperTriageItem] = {}
        for it in parsed.items:
            raw_id = it.arxiv_id.strip()
            by_id[raw_id] = it
            canon_id, _ = canonicalize_arxiv_id(raw_id)
            by_id.setdefault(canon_id, it)
        matched: list[tuple[TriagePaperInput, FlashPaperTriageItem]] = []
        missing_papers: list[TriagePaperInput] = []
        for p in papers:
            it = by_id.get(p.arxiv_id)
            if it is not None:
                matched.append((p, it))
                result.succeeded_ids.append(p.arxiv_id)
            else:
                missing_papers.append(p)

        if writer is not None and matched:
            self._persist_items(
                matched=matched,
                rubric_pack=rubric_pack,
                writer=writer,
                run_id=run_id,
            )

        # Retry any IDs omitted by Flash in a compact retry call (up to 1 pass)
        if missing_papers:
            if allow_bisect and len(missing_papers) < len(papers):
                sub = self.score_abstract_batch(
                    papers=missing_papers,
                    rubric_pack=rubric_pack,
                    writer=writer,
                    run_id=run_id,
                    allow_bisect=False,
                )
                result.succeeded_ids.extend(sub.succeeded_ids)
                result.missing_ids.extend(sub.missing_ids)
                result.permanent_failed.update(sub.permanent_failed)
                result.transient_failed.update(sub.transient_failed)
                result.input_tokens += sub.input_tokens
                result.output_tokens += sub.output_tokens
                result.estimated_cost_usd += sub.estimated_cost_usd
                result.latency_ms += sub.latency_ms
            else:
                for p in missing_papers:
                    result.missing_ids.append(p.arxiv_id)
                    result.transient_failed[p.arxiv_id] = (
                        0,
                        f"Flash omitted arxiv_id {p.arxiv_id} from batch response",
                    )

        return result
