"""Gemini Decision 1 gateway (POST /v1beta/decisions) for Stage 1 triage, calibration, and Stage 3 sweeps."""

from __future__ import annotations

import json
import math
import random
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import requests
from google import genai
from google.genai import errors as genai_errors

from arxiv_bench.config import Settings
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.schemas import RubricPack

DECISION_COST_PER_1M_INPUT_USD = 0.10
MAX_DECISION_INPUT_TOKENS = 200_000
APPROX_CHARS_PER_TOKEN = 4
DEFAULT_DECISION_TIMEOUT_MS = 90_000


class PermanentDecisionError(RuntimeError):
    """Non-retryable decision failure (e.g., 400 invalid input or content-filter empty response)."""

    def __init__(self, message: str, *, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code


class DailyQuotaExceededError(RuntimeError):
    """Raised when Gemini API returns a daily (RPD) quota exhaustion 429."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.status_code = 429


def is_daily_quota_error(exc: BaseException, status: int | None = None) -> bool:
    """Return True if an exception represents a daily (RPD) quota exhaustion."""
    if isinstance(exc, DailyQuotaExceededError):
        return True
    st = status if status is not None else _extract_status_code(exc)
    if st != 429:
        return False
    lowered = str(exc).lower()
    return any(
        tok in lowered
        for tok in (
            "requests per day",
            "requestsperday",
            "per day on tier",
            "daily limit",
            "perdayperproject",
            "per_day",
        )
    )


def classify_decision_error(exc: BaseException) -> tuple[bool, int, str]:
    """Return (is_permanent, http_status, short_detail) for triage error handling."""
    status = _extract_status_code(exc)
    detail = f"{type(exc).__name__}: {str(exc)[:300]}"
    lowered = detail.lower()
    if isinstance(exc, PermanentDecisionError):
        return True, status or exc.status_code, detail
    if status in (400, 422):
        return True, status, detail
    if status not in (401, 403, 429, 500, 502, 503, 504) and any(
        tok in lowered
        for tok in (
            "invalid_argument",
            "invalid argument",
            "content_filter",
            "prohibited_content",
            "safety",
            "blocked",
        )
    ):
        return True, status or 400, detail
    return False, status, detail


def _is_retryable_network_error(exc: BaseException, status: int) -> bool:
    if is_daily_quota_error(exc, status):
        return False
    if status in (429, 500, 502, 503, 504):
        return True
    if status != 0 or isinstance(exc, PermanentDecisionError):
        return False
    if isinstance(exc, (requests.RequestException, TimeoutError, ConnectionError, OSError)):
        return True
    name = type(exc).__name__.lower()
    return any(
        tok in name
        for tok in ("timeout", "connect", "protocol", "network", "readerror", "writeerror", "pool")
    )


@dataclass(frozen=True)
class DecisionAnswerRecord:
    """Normalized answer returned by gemini-decision-1 for a single rubric question."""

    question_id: str
    choice_or_value: str
    probability: float
    entropy: float
    distribution: dict[str, float]


@dataclass
class DecisionCallOutput:
    """Parsed decision response along with usage telemetry."""

    answers: list[DecisionAnswerRecord]
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    latency_ms: int
    http_status: int
    truncated_input: bool = False


@dataclass
class CalibrationPoint:
    """Precision/recall/F1 at a candidate probability threshold."""

    threshold: float
    tp: int
    fp: int
    fn: int
    tn: int
    precision: float
    recall: float
    f1: float


@dataclass
class CalibrationReport:
    """Summary returned by the mandatory Stage 0 gemini-decision-1 calibration gate."""

    sample_size: int
    succeeded: int
    failed: int
    transport_used: str
    observed_rpm: float
    observed_tpm: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    mean_entropy: float
    total_input_tokens: int
    estimated_cost_usd: float
    sample_errors: list[str] = field(default_factory=list)
    threshold_curve: list[CalibrationPoint] = field(default_factory=list)


def compute_shannon_entropy(distribution: dict[str, float]) -> float:
    """Compute base-2 Shannon entropy over a discrete probability distribution."""
    entropy = 0.0
    for prob in distribution.values():
        if prob > 0.0:
            entropy -= prob * math.log2(prob)
    return round(entropy, 6)


def trim_for_decision_context(
    text: str,
    *,
    max_tokens: int = MAX_DECISION_INPUT_TOKENS,
) -> tuple[str, bool]:
    """Enforce a strict <200,000-token context guard beneath gemini-decision-1's 262k limit."""
    max_chars = max_tokens * APPROX_CHARS_PER_TOKEN
    if len(text) <= max_chars:
        return text, False
    marker = "\n\n[TRUNCATED_FOR_DECISION_CONTEXT_LIMIT]\n"
    trimmed = text[: max_chars - len(marker)] + marker
    return trimmed, True


def format_structured_summary(extraction_json: str | None) -> str:
    """Format compact structured Stage 2 extraction metadata (URLs, facets, limitations) for Stage 3."""
    if not extraction_json:
        return ""
    try:
        data = json.loads(extraction_json)
    except Exception:  # noqa: BLE001
        return ""
    if not isinstance(data, dict):
        return ""

    lines: list[str] = []
    contrib = data.get("contribution_type")
    if contrib:
        lines.append(f"Contribution Type: {contrib}")
    benches = data.get("benchmarks") or []
    if isinstance(benches, list) and benches:
        b_items: list[str] = []
        for b in benches[:12]:
            if not isinstance(b, dict):
                continue
            name = b.get("name") or ""
            role = b.get("role") or ""
            url = b.get("url") or ""
            part = f"{name} ({role})" if role else str(name)
            if url:
                part += f" [URL: {url}]"
            if part.strip():
                b_items.append(part.strip())
        if b_items:
            lines.append("Benchmarks & Artifacts: " + "; ".join(b_items))
    for key, label in (
        ("modalities", "Modalities"),
        ("domains", "Domains"),
        ("tasks", "Tasks"),
        ("evaluation_methods", "Evaluation Methods"),
        ("languages", "Languages"),
        ("base_benchmarks", "Base Benchmarks"),
    ):
        vals = data.get(key)
        if isinstance(vals, list) and vals:
            lines.append(f"{label}: {', '.join(str(v) for v in vals[:15])}")
    if data.get("is_continuous_testing") is not None:
        lines.append(f"Continuous Testing: {bool(data['is_continuous_testing'])}")
    lim = data.get("stated_limitations")
    if lim:
        lines.append(f"Stated Limitations: {str(lim)[:600]}")
    return "\n".join(lines)


def _normalize_model_name(model: str) -> str:
    return model if model.startswith("models/") else f"models/{model}"


def _extract_status_code(exc: BaseException) -> int:
    for attr in ("code", "status_code"):
        val = getattr(exc, attr, None)
        if isinstance(val, int):
            return val
    resp = getattr(exc, "response", None)
    if resp is not None and isinstance(getattr(resp, "status_code", None), int):
        return int(resp.status_code)
    return 500


def _parse_answers_dict(raw_answers: dict[str, Any]) -> list[DecisionAnswerRecord]:
    """Parse SDK Pydantic or raw REST JSON decision answers into uniform records."""
    parsed: list[DecisionAnswerRecord] = []
    for qid, ans in raw_answers.items():
        if hasattr(ans, "model_dump"):
            ans_dict = ans.model_dump()
        elif isinstance(ans, dict):
            ans_dict = ans
        else:
            continue

        ans_type = ans_dict.get("type")
        if ans_type == "noul" or "noul" in ans_dict:
            p_true = float(ans_dict["noul"])
            p_false = max(0.0, min(1.0, 1.0 - p_true))
            dist = {"true": round(p_true, 6), "false": round(p_false, 6)}
            choice = "true" if p_true >= 0.5 else "false"
            parsed.append(
                DecisionAnswerRecord(
                    question_id=qid,
                    choice_or_value=choice,
                    probability=round(p_true, 6),
                    entropy=compute_shannon_entropy(dist),
                    distribution=dist,
                )
            )
        elif ans_type == "choice" or "choice" in ans_dict:
            choice = str(ans_dict["choice"])
            probs = {str(k): float(v) for k, v in (ans_dict.get("probabilities") or {}).items()}
            p_win = float(ans_dict.get("confidence", probs.get(choice, 0.0)))
            parsed.append(
                DecisionAnswerRecord(
                    question_id=qid,
                    choice_or_value=choice,
                    probability=round(p_win, 6),
                    entropy=compute_shannon_entropy(probs),
                    distribution=probs,
                )
            )
        elif ans_type == "score" or "score" in ans_dict:
            score_val = float(ans_dict["score"])
            probs = {str(k): float(v) for k, v in (ans_dict.get("probabilities") or {}).items()}
            p_win = float(ans_dict.get("confidence", max(probs.values(), default=0.0)))
            parsed.append(
                DecisionAnswerRecord(
                    question_id=qid,
                    choice_or_value=f"{score_val:.4f}",
                    probability=round(p_win, 6),
                    entropy=compute_shannon_entropy(probs),
                    distribution=probs,
                )
            )
    return parsed


class DecisionClient:
    """Thread-safe gemini-decision-1 client supporting SDK and REST fallback."""

    def __init__(
        self,
        settings: Settings,
        *,
        client: Any | None = None,
        http_session: requests.Session | None = None,
        max_retries: int = 6,
        prefer_rest: bool = True,
        max_rpm: float | None = None,
    ) -> None:
        self._settings = settings
        self._client = client
        self._prefer_rest = prefer_rest
        self._client_lock = threading.Lock()
        self._stats_lock = threading.Lock()
        self._pace_lock = threading.Lock()
        self._min_interval_s = (60.0 / max_rpm) if (max_rpm and max_rpm > 0) else 0.0
        self._next_allowed_at = 0.0
        self._cooldown_until = 0.0
        if http_session is not None:
            self._http = http_session
        else:
            sess = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=128, pool_maxsize=128)
            sess.mount("https://", adapter)
            sess.mount("http://", adapter)
            self._http = sess
        self._max_retries = max_retries
        self.transport_used = "rest" if (prefer_rest and client is None) else "sdk"
        self.retry_429_count = 0
        self.retry_5xx_count = 0
        self.retry_network_count = 0
        self.daily_quota_error: str | None = None

    def _wait_for_slot(self) -> None:
        """Smoothly pace requests under max_rpm and honor any shared 429 cooldown."""
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

    def _get_sdk_client(self) -> Any:
        if self._client is None:
            with self._client_lock:
                if self._client is None:
                    if not self._settings.google_api_key:
                        raise RuntimeError("GOOGLE_API_KEY is required for DecisionClient.")
                    self._client = genai.Client(
                        api_key=self._settings.google_api_key,
                        http_options={
                            "api_version": "v1beta",
                            "timeout": DEFAULT_DECISION_TIMEOUT_MS,
                        },
                    )
        return self._client

    def evaluate(
        self,
        *,
        input_text: str,
        rubric_pack: RubricPack,
        arxiv_id: str | None = None,
        stage: str = "triage",
        run_id: str | None = None,
        writer: SingleWriterQueue | None = None,
    ) -> DecisionCallOutput:
        """Evaluate all questions in a RubricPack against a single paper's input context."""
        bounded_input, was_truncated = trim_for_decision_context(input_text)
        model_name = _normalize_model_name(rubric_pack.model or self._settings.decision_model)
        questions_payload = {q.id: q.to_decision_param() for q in rubric_pack.questions}

        last_exc: BaseException | None = None
        for attempt in range(self._max_retries):
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)
            self._wait_for_slot()
            if self.daily_quota_error is not None:
                raise DailyQuotaExceededError(self.daily_quota_error)
            t0 = time.monotonic()
            try:
                raw_answers, input_tokens, output_tokens, http_status = self._invoke_decisions_api(
                    model_name=model_name,
                    input_text=bounded_input,
                    questions=questions_payload,
                )
                latency_ms = int((time.monotonic() - t0) * 1000)
                parsed_answers = _parse_answers_dict(raw_answers)
                if not parsed_answers:
                    raise PermanentDecisionError(
                        "Empty answers returned by decisions API (possible safety filter)",
                        status_code=422,
                    )
                if input_tokens <= 0:
                    input_tokens = max(1, len(bounded_input) // APPROX_CHARS_PER_TOKEN)
                cost_usd = (input_tokens / 1_000_000.0) * DECISION_COST_PER_1M_INPUT_USD
                output = DecisionCallOutput(
                    answers=parsed_answers,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost_usd=cost_usd,
                    latency_ms=latency_ms,
                    http_status=http_status,
                    truncated_input=was_truncated,
                )
                if writer is not None:
                    self._log_api_call(
                        writer,
                        run_id=run_id,
                        stage=stage,
                        model=model_name,
                        arxiv_id=arxiv_id,
                        output=output,
                    )
                return output
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
                        ) VALUES (?, ?, 'v1beta/decisions', ?, ?, 0, 0, 0.0, ?, ?, ?)
                        """,
                        (
                            run_id,
                            stage,
                            model_name,
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
                    backoff = min(35.0, (2.5 * (2**attempt))) + random.uniform(0.5, 2.5)
                    time.sleep(backoff)
                    continue
                raise

        assert last_exc is not None
        raise last_exc

    def _invoke_decisions_api(
        self,
        *,
        model_name: str,
        input_text: str,
        questions: dict[str, dict[str, object]],
    ) -> tuple[dict[str, Any], int, int, int]:
        if not (self._prefer_rest and self._client is None):
            sdk = self._get_sdk_client()
            if hasattr(sdk, "decisions") and hasattr(sdk.decisions, "create"):
                self.transport_used = "sdk"
                resp = sdk.decisions.create(
                    model=model_name,
                    input=input_text,
                    questions=questions,
                )
                answers = getattr(resp, "answers", None) or {}
                usage = getattr(resp, "usage", None)
                in_tok = int(getattr(usage, "total_input_tokens", 0) or 0)
                out_tok = int(getattr(usage, "total_output_tokens", 0) or 0)
                return answers, in_tok, out_tok, 200

        # Direct pooled REST transport (avoids SyncHttpx2Client HTTP/2 thread pool stalls)
        if not self._settings.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is required for DecisionClient.")
        self.transport_used = "rest"
        resp = self._http.post(
            "https://generativelanguage.googleapis.com/v1beta/decisions",
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self._settings.google_api_key,
            },
            json={
                "model": model_name,
                "input": input_text,
                "questions": questions,
            },
            timeout=90,
        )
        if resp.status_code >= 400:
            err_body = (resp.text or "").strip().replace("\n", " ")[:300]
            err = requests.HTTPError(
                f"{resp.status_code} {resp.reason}: {err_body}",
                response=resp,
            )
            raise err
        body = resp.json()
        usage = body.get("usage") or {}
        return (
            body.get("answers") or {},
            int(usage.get("total_input_tokens", 0) or 0),
            int(usage.get("total_output_tokens", 0) or 0),
            resp.status_code,
        )

    def _log_api_call(
        self,
        writer: SingleWriterQueue,
        *,
        run_id: str | None,
        stage: str,
        model: str,
        arxiv_id: str | None,
        output: DecisionCallOutput,
    ) -> None:
        writer.submit_sql(
            """
            INSERT INTO api_call_logs (
                run_id, stage, endpoint, model, arxiv_id,
                prompt_tokens, output_tokens, estimated_cost_usd,
                latency_ms, http_status, created_at
            ) VALUES (?, ?, 'v1beta/decisions', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                stage,
                model,
                arxiv_id,
                output.input_tokens,
                output.output_tokens,
                output.estimated_cost_usd,
                output.latency_ms,
                output.http_status,
                datetime.now(UTC).isoformat(),
            ),
        )

    def score_abstract(
        self,
        *,
        arxiv_id: str,
        paper_version: int,
        title: str,
        abstract: str,
        categories: list[str] | str,
        rubric_pack: RubricPack,
        writer: SingleWriterQueue | None = None,
        run_id: str | None = None,
    ) -> DecisionCallOutput:
        """Stage 1 single-paper abstract triage persisting calibrated probabilities."""
        cat_str = " ".join(categories) if isinstance(categories, list) else str(categories or "")
        input_text = f"Title: {title}\nCategories: {cat_str}\nAbstract:\n{abstract}"
        output = self.evaluate(
            input_text=input_text,
            rubric_pack=rubric_pack,
            arxiv_id=arxiv_id,
            stage="triage",
            run_id=run_id,
            writer=writer,
        )
        if writer is not None:
            now_iso = datetime.now(UTC).isoformat()
            model_name = _normalize_model_name(rubric_pack.model or self._settings.decision_model)
            rows_to_write = [
                (
                    arxiv_id,
                    paper_version,
                    rubric_pack.rubric_id,
                    rubric_pack.rubric_version,
                    ans.question_id,
                    model_name,
                    ans.choice_or_value,
                    ans.probability,
                    json.dumps(ans.distribution),
                    now_iso,
                )
                for ans in output.answers
            ]

            def _persist_triage(cur: sqlite3.Cursor) -> None:
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
                    rows_to_write,
                )
                cur.execute(
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
                    (arxiv_id, run_id, now_iso),
                )

            writer.submit(_persist_triage)
        return output

    def score_rubric_pack(
        self,
        *,
        arxiv_id: str,
        title: str,
        abstract: str,
        evidence_card: str,
        body_text: str = "",
        structured_summary: str = "",
        rubric_pack: RubricPack,
        writer: SingleWriterQueue | None = None,
        run_id: str | None = None,
    ) -> DecisionCallOutput:
        """Stage 3 on-demand gap-rubric sweep over stored Evidence Card (+ optional full text)."""
        parts = [f"Title: {title}", f"Abstract:\n{abstract}"]
        if structured_summary:
            parts.append(f"Structured Extracted Metadata:\n{structured_summary}")
        if evidence_card:
            parts.append(f"Structured Benchmark Evidence Card:\n{evidence_card}")
        if body_text:
            parts.append(f"Paper Text (Bibliography Trimmed):\n{body_text}")
        context = "\n\n".join(parts)
        output = self.evaluate(
            input_text=context,
            rubric_pack=rubric_pack,
            arxiv_id=arxiv_id,
            stage=f"score:{rubric_pack.rubric_id}",
            run_id=run_id,
            writer=writer,
        )
        if writer is not None and output.answers:
            now_iso = datetime.now(UTC).isoformat()
            model_name = _normalize_model_name(rubric_pack.model or self._settings.decision_model)
            score_rows = [
                (
                    arxiv_id,
                    rubric_pack.rubric_id,
                    rubric_pack.rubric_version,
                    ans.question_id,
                    model_name,
                    ans.choice_or_value,
                    ans.probability,
                    ans.entropy,
                    json.dumps(ans.distribution),
                    1 if output.truncated_input else 0,
                    now_iso,
                )
                for ans in output.answers
            ]

            def _persist_scores(
                cur: sqlite3.Cursor,
                _rows: list[tuple[Any, ...]] = score_rows,
            ) -> None:
                cur.executemany(
                    """
                    INSERT INTO decision_scores (
                        arxiv_id, rubric_id, rubric_version, question_id,
                        model_id, choice_or_score, probability, entropy,
                        distribution_json, truncated_input, scored_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(arxiv_id, rubric_id, rubric_version, question_id)
                    DO UPDATE SET
                        model_id = excluded.model_id,
                        choice_or_score = excluded.choice_or_score,
                        probability = excluded.probability,
                        entropy = excluded.entropy,
                        distribution_json = excluded.distribution_json,
                        truncated_input = excluded.truncated_input,
                        scored_at = excluded.scored_at
                    """,
                    _rows,
                )

            writer.submit(_persist_scores)
        return output

    def run_calibration(
        self,
        conn: sqlite3.Connection,
        rubric_pack: RubricPack,
        *,
        sample_size: int = 300,
        workers: int = 8,
        writer: SingleWriterQueue | None = None,
        run_id: str | None = None,
    ) -> CalibrationReport:
        """Run Stage 0 calibration gate measuring live RPM/TPM and precision/recall cutoffs."""
        half = max(1, sample_size // 2)
        positives = conn.execute(
            """
            SELECT arxiv_id, COALESCE(latest_version_seen, 1) AS paper_version,
                   title, abstract, categories_json,
                   json_extract(legacy_metadata_json, '$.is_benchmark') AS legacy_is_bench
            FROM papers
            WHERE title IS NOT NULL AND abstract IS NOT NULL AND abstract != ''
              AND json_extract(legacy_metadata_json, '$.is_benchmark') = 1
            ORDER BY ((rowid * 2654435761) & 2147483647), arxiv_id
            LIMIT ?
            """,
            (half,),
        ).fetchall()
        need_neg = sample_size - len(positives)
        negatives = conn.execute(
            """
            SELECT arxiv_id, COALESCE(latest_version_seen, 1) AS paper_version,
                   title, abstract, categories_json,
                   json_extract(legacy_metadata_json, '$.is_benchmark') AS legacy_is_bench
            FROM papers
            WHERE title IS NOT NULL AND abstract IS NOT NULL AND abstract != ''
              AND json_extract(legacy_metadata_json, '$.is_benchmark') = 0
            ORDER BY ((rowid * 2654435761) & 2147483647), arxiv_id
            LIMIT ?
            """,
            (need_neg,),
        ).fetchall()
        if len(negatives) < need_neg:
            fallback = conn.execute(
                """
                SELECT arxiv_id, COALESCE(latest_version_seen, 1) AS paper_version,
                       title, abstract, categories_json,
                       0 AS legacy_is_bench
                FROM papers
                WHERE title IS NOT NULL AND abstract IS NOT NULL AND abstract != ''
                  AND json_extract(legacy_metadata_json, '$.is_benchmark') IS NULL
                ORDER BY ((rowid * 2654435761) & 2147483647), arxiv_id
                LIMIT ?
                """,
                (need_neg - len(negatives),),
            ).fetchall()
            negatives = list(negatives) + list(fallback)
        rows = list(positives) + list(negatives)
        if not rows:
            return CalibrationReport(
                sample_size=0,
                succeeded=0,
                failed=0,
                transport_used=self.transport_used,
                observed_rpm=0.0,
                observed_tpm=0.0,
                avg_latency_ms=0.0,
                p50_latency_ms=0.0,
                p95_latency_ms=0.0,
                mean_entropy=0.0,
                total_input_tokens=0,
                estimated_cost_usd=0.0,
            )

        t_start = time.monotonic()
        scored: list[tuple[bool, float]] = []
        latencies: list[int] = []
        entropies: list[float] = []
        sample_errors: list[str] = []
        total_tokens = 0
        total_cost = 0.0
        failed = 0

        def _eval_row(r: sqlite3.Row) -> tuple[bool, DecisionCallOutput]:
            cats = json.loads(r["categories_json"]) if r["categories_json"] else []
            out = self.score_abstract(
                arxiv_id=r["arxiv_id"],
                paper_version=int(r["paper_version"] or 1),
                title=r["title"] or "",
                abstract=r["abstract"] or "",
                categories=cats,
                rubric_pack=rubric_pack,
                writer=writer,
                run_id=run_id,
            )
            return bool(r["legacy_is_bench"]), out

        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futs = [pool.submit(_eval_row, r) for r in rows]
            for fut in as_completed(futs):
                try:
                    gold, out = fut.result()
                    latencies.append(out.latency_ms)
                    total_tokens += out.input_tokens
                    total_cost += out.estimated_cost_usd
                    prob = 0.0
                    for ans in out.answers:
                        if ans.question_id == "is_benchmark_contribution":
                            prob = ans.probability
                            entropies.append(ans.entropy)
                            break
                    scored.append((gold, prob))
                except Exception as exc:  # noqa: BLE001
                    failed += 1
                    msg = f"{type(exc).__name__}: {str(exc)[:180]}"
                    if len(sample_errors) < 5 and msg not in sample_errors:
                        sample_errors.append(msg)

        if writer is not None:
            writer.flush()

        elapsed_min = max(1e-6, (time.monotonic() - t_start) / 60.0)
        succeeded = len(scored)
        sorted_lat = sorted(latencies)
        p50 = float(sorted_lat[len(sorted_lat) // 2]) if sorted_lat else 0.0
        p95 = (
            float(sorted_lat[min(len(sorted_lat) - 1, int(len(sorted_lat) * 0.95))])
            if sorted_lat
            else 0.0
        )
        mean_h = round(sum(entropies) / len(entropies), 4) if entropies else 0.0

        curve: list[CalibrationPoint] = []
        for step in range(1, 10):
            thr = round(step * 0.1, 2)
            tp = sum(1 for gold, p in scored if gold and p >= thr)
            fp = sum(1 for gold, p in scored if not gold and p >= thr)
            fn = sum(1 for gold, p in scored if gold and p < thr)
            tn = sum(1 for gold, p in scored if not gold and p < thr)
            prec = tp / (tp + fp) if (tp + fp) else 0.0
            rec = tp / (tp + fn) if (tp + fn) else 0.0
            f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
            curve.append(
                CalibrationPoint(
                    threshold=thr,
                    tp=tp,
                    fp=fp,
                    fn=fn,
                    tn=tn,
                    precision=round(prec, 4),
                    recall=round(rec, 4),
                    f1=round(f1, 4),
                )
            )

        return CalibrationReport(
            sample_size=len(rows),
            succeeded=succeeded,
            failed=failed,
            transport_used=self.transport_used,
            observed_rpm=round(succeeded / elapsed_min, 2),
            observed_tpm=round(total_tokens / elapsed_min, 2),
            avg_latency_ms=round(sum(latencies) / len(latencies), 1) if latencies else 0.0,
            p50_latency_ms=p50,
            p95_latency_ms=p95,
            mean_entropy=mean_h,
            total_input_tokens=total_tokens,
            estimated_cost_usd=round(total_cost, 6),
            sample_errors=sample_errors,
            threshold_curve=curve,
        )
