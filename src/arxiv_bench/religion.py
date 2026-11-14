"""Preserved downstream religious-bias research module backed purely by SQLite."""

from __future__ import annotations

import csv
import json
import logging
import random
import sqlite3
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

from arxiv_bench.config import Settings, get_arxiv_url
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.decision_client import (
    _extract_status_code,
    _is_retryable_network_error,
    _normalize_model_name,
    is_daily_quota_error,
)
from arxiv_bench.extract_client import INLINE_PDF_MAX_BYTES
from arxiv_bench.flash_triage import flash_cost_rates_per_1m
from arxiv_bench.pdf_storage import PdfStorageManager, WithdrawnPaperError, decompress_text
from arxiv_bench.schemas import (
    BiasTargetsExtraction,
    ReligiousBiasDetailExtraction,
)

# Canonical religious group normalization preserved from legacy generate_full_analysis.py
RELIGIOUS_GROUP_NORMALIZATION: dict[str, str] = {
    "christian": "Christianity",
    "christians": "Christianity",
    "christianity": "Christianity",
    "catholic": "Catholic",
    "catholicism": "Catholic",
    "roman catholic": "Catholic",
    "protestant": "Protestant",
    "protestantism": "Protestant",
    "orthodox": "Orthodox",
    "eastern orthodox": "Orthodox",
    "greek orthodox": "Orthodox",
    "russian orthodox": "Orthodox",
    "baptist": "Baptist",
    "methodist": "Methodist",
    "evangelical": "Evangelical",
    "evangelicalism": "Evangelical",
    "mormon": "Mormon",
    "mormonism": "Mormon",
    "lutheran": "Lutheran",
    "lutheranism": "Lutheran",
    "pentecostal": "Pentecostal",
    "pentecostalism": "Pentecostal",
    "anglican": "Anglican",
    "anglicanism": "Anglican",
    "presbyterian": "Presbyterian",
    "muslim": "Islam",
    "muslims": "Islam",
    "islam": "Islam",
    "sunni": "Sunni",
    "sunni islam": "Sunni",
    "shia": "Shia",
    "shia islam": "Shia",
    "shiite": "Shia",
    "sufi": "Sufi",
    "sufism": "Sufi",
    "jewish": "Judaism",
    "judaism": "Judaism",
    "jews": "Judaism",
    "buddhist": "Buddhism",
    "buddhism": "Buddhism",
    "buddhists": "Buddhism",
    "hindu": "Hinduism",
    "hindus": "Hinduism",
    "hinduism": "Hinduism",
    "sikh": "Sikhism",
    "sikhs": "Sikhism",
    "sikhism": "Sikhism",
    "atheist": "Atheism",
    "atheists": "Atheism",
    "atheism": "Atheism",
    "agnostic": "Agnosticism",
    "agnostics": "Agnosticism",
    "agnosticism": "Agnosticism",
    "confucian": "Confucianism",
    "confucianism": "Confucianism",
    "taoism": "Taoism",
    "daoism": "Taoism",
    "taoist": "Taoism",
    "daoist": "Taoism",
    "shinto": "Shinto",
    "shintoism": "Shinto",
    "jain": "Jainism",
    "jainism": "Jainism",
    "zoroastrian": "Zoroastrianism",
    "zoroastrianism": "Zoroastrianism",
    "religion": "Religion (general)",
    "religion (general)": "Religion (general)",
    "religion (unspecified)": "Religion (general)",
    "religion (as a general category)": "Religion (general)",
    "religion (general category)": "Religion (general)",
    "religious studies": "Religion (general)",
    "world religions": "Religion (general)",
    "world religion": "Religion (general)",
    "other religions": "Religion (general)",
    "no religion": "Non-religious",
    "secular": "Non-religious",
    "not specified": "Not specified",
}

# Canonical bias target normalization preserved verbatim from scripts/analyze_bias_targets.py
BIAS_TARGET_NORMALIZATION: dict[str, str] = {
    # Gender
    "gender bias": "Gender bias",
    "gender": "Gender bias",
    "sex bias": "Gender bias",
    "sex/gender bias": "Gender bias",
    "sexism": "Gender bias",
    "sexism and gender bias": "Gender bias",
    "misogyny and gender bias": "Gender bias",
    "gender bias (sexism)": "Gender bias",
    "gender bias (misogyny)": "Gender bias",
    "gender identity bias": "Gender bias",
    # Racial/Ethnic
    "racial bias": "Racial/Ethnic bias",
    "race bias": "Racial/Ethnic bias",
    "racism": "Racial/Ethnic bias",
    "ethnic bias": "Racial/Ethnic bias",
    "ethnicity bias": "Racial/Ethnic bias",
    "racial/ethnic bias": "Racial/Ethnic bias",
    "racial and ethnic bias": "Racial/Ethnic bias",
    "racial, ethnic, and nationality bias": "Racial/Ethnic bias",
    "racial/ethnicity bias": "Racial/Ethnic bias",
    "racial and ethnicity bias": "Racial/Ethnic bias",
    "racial and nationality bias": "Racial/Ethnic bias",
    "skin tone bias": "Racial/Ethnic bias",
    "skin color bias": "Racial/Ethnic bias",
    # Religious
    "religious bias": "Religious bias",
    "religion bias": "Religious bias",
    "cultural and religious bias": "Religious bias",
    # Age
    "age bias": "Age bias",
    "ageism": "Age bias",
    # Political/Ideological
    "political bias": "Political bias",
    "politics bias": "Political bias",
    "geopolitical bias": "Political bias",
    "ideological and political bias": "Political bias",
    "socio-political bias": "Political bias",
    "ideological bias": "Political bias",
    "political and ideological bias": "Political bias",
    "political/ideological bias": "Political bias",
    "viewpoint bias": "Political bias",
    "stance bias": "Political bias",
    # Nationality
    "nationality bias": "Nationality bias",
    "national bias": "Nationality bias",
    "country bias": "Nationality bias",
    # Cultural
    "cultural bias": "Cultural bias",
    "culture bias": "Cultural bias",
    "geo-cultural bias": "Cultural bias",
    "cultural and language bias": "Cultural bias",
    "cultural and linguistic bias": "Cultural bias",
    "cultural and nationality bias": "Cultural bias",
    "language and cultural bias": "Cultural bias",
    # Geographic
    "geographic bias": "Geographic bias",
    "geographical bias": "Geographic bias",
    "geographic/nationality bias": "Geographic bias",
    "geographic and cultural bias": "Geographic bias",
    "location bias": "Geographic bias",
    "geospatial bias": "Geographic bias",
    "spatial bias": "Geographic bias",
    # Language/Linguistic
    "language bias": "Language bias",
    "linguistic bias": "Language bias",
    "dialect bias": "Language bias",
    "dialect/language bias": "Language bias",
    "language and dialect bias": "Language bias",
    "language/dialect bias": "Language bias",
    "dialectal bias": "Language bias",
    "accent bias": "Language bias",
    "lexical bias": "Language bias",
    # Position/Positional
    "position bias": "Position bias",
    "positional bias": "Position bias",
    # Sexual orientation / LGBTQ+
    "sexual orientation bias": "Sexual orientation bias",
    "lgbtq+ bias": "Sexual orientation bias",
    "lgbtq bias": "Sexual orientation bias",
    "homophobia": "Sexual orientation bias",
    "gender and sexual orientation bias": "Sexual orientation bias",
    "gender/sexual orientation bias": "Sexual orientation bias",
    "orientation bias": "Sexual orientation bias",
    "sexual orientation and gender identity bias": "Sexual orientation bias",
    # Socioeconomic
    "socioeconomic bias": "Socioeconomic bias",
    "socio-economic bias": "Socioeconomic bias",
    "economic bias": "Socioeconomic bias",
    "class bias": "Socioeconomic bias",
    "class and socioeconomic bias": "Socioeconomic bias",
    "socioeconomic status bias": "Socioeconomic bias",
    # Disability
    "disability bias": "Disability bias",
    "ableism": "Disability bias",
    "ability bias": "Disability bias",
    # Physical appearance
    "physical appearance bias": "Physical appearance bias",
    "appearance bias": "Physical appearance bias",
    "body type bias": "Physical appearance bias",
    "weight bias": "Physical appearance bias",
    # Occupational
    "occupational bias": "Occupational bias",
    "profession bias": "Occupational bias",
    "occupational/socioeconomic bias": "Occupational bias",
    "occupation bias": "Occupational bias",
    "professional bias": "Occupational bias",
    # Hate speech / Toxicity
    "hate speech detection": "Hate speech/Toxicity",
    "hate speech detection (general toxic or hateful content)": "Hate speech/Toxicity",
    "toxic content": "Hate speech/Toxicity",
    "toxicity": "Hate speech/Toxicity",
    "toxicity bias": "Hate speech/Toxicity",
    "hate speech": "Hate speech/Toxicity",
    "toxicity and hate speech": "Hate speech/Toxicity",
    # Stereotyping
    "stereotyping": "Stereotyping",
    "stereotype bias": "Stereotyping",
    "stereotypes": "Stereotyping",
    "social bias": "Stereotyping",
    "stereotypical bias": "Stereotyping",
    # Fairness
    "fairness in outcomes": "Fairness",
    "fairness": "Fairness",
    "outcome fairness": "Fairness",
    # Length / Verbosity
    "length bias": "Length bias",
    "verbosity bias": "Length bias",
    "length bias (verbosity bias)": "Length bias",
    # Self-preference / Self-bias
    "self-preference bias": "Self-preference bias",
    "self preference bias": "Self-preference bias",
    "self-enhancement bias": "Self-preference bias",
    "self-bias": "Self-preference bias",
    "self-evaluation bias": "Self-preference bias",
    # Regional
    "regional bias": "Regional bias",
    "regional language bias": "Regional bias",
    # Annotation/Annotator
    "annotator bias": "Annotator bias",
    "annotation bias": "Annotator bias",
    # Educational
    "educational bias": "Educational bias",
    "education bias": "Educational bias",
    "educational background bias": "Educational bias",
    # Sycophancy
    "sycophancy bias": "Sycophancy bias",
    "sycophancy": "Sycophancy bias",
    "sycophantic bias": "Sycophancy bias",
    # Cognitive
    "cognitive bias": "Cognitive bias",
    "cognitive biases": "Cognitive bias",
    "confirmation bias": "Cognitive bias",
    "anchoring bias": "Cognitive bias",
    "recency bias": "Cognitive bias",
    "authority bias": "Cognitive bias",
    "conformity bias": "Cognitive bias",
    # Demographic (broad)
    "demographic bias": "Demographic bias",
    "sociodemographic bias": "Demographic bias",
    "social and demographic bias": "Demographic bias",
    # Intersectional
    "intersectional bias": "Intersectional bias",
    "intergroup bias": "Intersectional bias",
    # Moral/Ethical
    "moral bias": "Moral/Ethical bias",
    "ethical and moral bias": "Moral/Ethical bias",
    "moral and ethical bias": "Moral/Ethical bias",
    # Sentiment
    "sentiment bias": "Sentiment bias",
    "positivity bias": "Sentiment bias",
    "social desirability bias": "Sentiment bias",
    # Caste
    "caste bias": "Caste bias",
    # Mental health
    "mental health bias": "Mental health bias",
    "health status bias": "Mental health bias",
    # Marital/Family status
    "marital status bias": "Marital status bias",
    # Immigration status
    "immigration status bias": "Immigration status bias",
    # Media
    "media bias": "Media bias",
    "reporting bias": "Media bias",
    "framing bias": "Media bias",
    # Evaluation/Scoring
    "evaluation bias": "Evaluation bias",
    "evaluator bias": "Evaluation bias",
    "scoring bias": "Evaluation bias",
    "evaluation metric bias": "Evaluation bias",
    "llm evaluator bias": "Evaluation bias",
    # Dataset/Methodological
    "dataset bias": "Dataset bias",
    "dataset artifact bias": "Dataset bias",
    "dataset bias (annotation artifacts)": "Dataset bias",
    "dataset bias (spurious correlations)": "Dataset bias",
    "spurious correlation bias": "Dataset bias",
    "spurious bias": "Dataset bias",
    "class imbalance bias": "Dataset bias",
    "data contamination bias": "Dataset bias",
    "sampling bias": "Dataset bias",
    "selection bias": "Dataset bias",
    "label bias": "Dataset bias",
    "historical bias": "Dataset bias",
    # Modality
    "modality bias": "Modality bias",
    "visual bias": "Modality bias",
    # Popularity
    "popularity bias": "Popularity bias",
    "brand bias": "Popularity bias",
    # Domain
    "domain bias": "Domain bias",
    "topic bias": "Domain bias",
    # Representation
    "representation bias": "Representation bias",
    "representational bias": "Representation bias",
    # Algorithmic
    "algorithmic bias": "Algorithmic bias",
    "general algorithmic bias": "Algorithmic bias",
    "automation bias": "Algorithmic bias",
    "inductive bias": "Algorithmic bias",
    # Identity
    "identity bias": "Identity bias",
    "name bias": "Identity bias",
    # Style/Response
    "response bias": "Response bias",
    "stylistic bias": "Response bias",
    "style bias": "Response bias",
    # General / Other
    "general bias": "General bias",
    "general social bias": "General bias",
    "societal bias": "General bias",
    # Primary target normalization
    "none": "No Primary Bias Target",
    "no primary bias target": "No Primary Bias Target",
    "n/a": "No Primary Bias Target",
}

_RELIGIOUS_KEYWORDS = (
    "relig",
    "faith",
    "spiritual",
    "theolog",
    "islam",
    "muslim",
    "christian",
    "jewish",
    "hindu",
    "buddhis",
    "sikh",
    "mormon",
    "latter-day",
    "antisemit",
)

NON_CS_CAT_DESCRIPTIONS: dict[str, str] = {
    "stat.ML": "Machine Learning (Statistics)",
    "stat.ME": "Methodology (Statistics)",
    "stat.AP": "Applications (Statistics)",
    "stat.TH": "Statistics Theory",
    "stat.CO": "Computation (Statistics)",
    "physics.soc-ph": "Physics and Society",
    "econ.TH": "Theoretical Economics",
    "econ.GN": "General Economics",
    "eess.AS": "Audio and Speech Processing",
    "eess.SP": "Signal Processing",
    "eess.IV": "Image and Video Processing",
    "math.IT": "Information Theory",
    "math.ST": "Statistics Theory (Math)",
    "math.OC": "Optimization and Control",
    "q-bio.NC": "Neurons and Cognition",
    "q-bio.QM": "Quantitative Methods (Q-Bio)",
    "q-fin.EC": "Economics (Quantitative Finance)",
}


@dataclass(frozen=True)
class ReligionReportCounts:
    """Parity metrics returned by generate_full_reports."""

    llm_bias_papers: int
    religion_papers: int
    religion_primary_papers: int
    reports_written: list[str]


def normalize_religious_group(group: str) -> str:
    return RELIGIOUS_GROUP_NORMALIZATION.get(group.strip().lower(), group.strip())


def normalize_model_name(model: str) -> str:
    cleaned = model.strip()
    if cleaned.upper() == "GPT-40":
        return "GPT-4o"
    return cleaned


_CANONICAL_BIAS_TARGETS_BY_LOWER: dict[str, str] = {
    v.lower(): v for v in BIAS_TARGET_NORMALIZATION.values()
}


def normalize_bias_target(target: str) -> str:
    cleaned = target.strip()
    if not cleaned:
        return cleaned
    low = cleaned.lower()
    mapped = BIAS_TARGET_NORMALIZATION.get(low)
    if mapped is not None:
        return mapped
    canonical = _CANONICAL_BIAS_TARGETS_BY_LOWER.get(low)
    if canonical is not None:
        return canonical
    return cleaned.title()


def check_mormon_mention(payload: dict[str, Any] | str) -> bool:
    text = payload.lower() if isinstance(payload, str) else json.dumps(payload).lower()
    return any(term in text for term in ("mormon", "latter-day", "lds"))


def _has_religious_target(targets: list[str], primary: str) -> bool:
    for txt in [*targets, primary]:
        low = txt.lower()
        if "faithfulness" in low:
            continue
        if any(kw in low for kw in _RELIGIOUS_KEYWORDS):
            return True
    return False


def _generate_markdown_table(
    counter: Counter[str],
    heading: str,
    col1: str,
    col2: str,
    *,
    limit: int | None = None,
    denominator: int | None = None,
    heading_level: int = 2,
) -> str:
    prefix = "#" * heading_level
    lines = [f"{prefix} {heading}\n"]
    if denominator and denominator > 0:
        lines.append(f"| {col1} | {col2} | % of {denominator} papers |")
        lines.append("|---|---:|---:|")
        for key, cnt in counter.most_common(limit):
            pct = (cnt / denominator) * 100.0
            if key == "Religious bias":
                lines.append(f"| **{key}** | **{cnt}** | **{pct:.1f}%** |")
            else:
                lines.append(f"| {key} | {cnt} | {pct:.1f}% |")
    else:
        lines.append(f"| {col1} | {col2} |")
        lines.append("|---|---:|")
        for key, cnt in counter.most_common(limit):
            if key == "Religious bias":
                lines.append(f"| **{key}** | **{cnt}** |")
            else:
                lines.append(f"| {key} | {cnt} |")
    lines.append("")
    return "\n".join(lines)


BIAS_TARGETS_PROMPT = """Analyze this academic paper and identify what types of bias are being measured or evaluated.

Return JSON matching the schema with these fields:
1. `bias_targets`: list of objects, each describing a bias type that the paper measures or evaluates:
   - `target`: concise descriptive category name (e.g., "Gender bias", "Racial bias", "Religious bias", "Age bias", "Political bias", "Nationality bias", "Socioeconomic bias", "Disability bias", "Sexual orientation bias", "Cultural bias", "Language bias").
   - `methodology`: brief description of how the paper measures or evaluates this bias.
   Include ALL bias types the paper measures. Return an empty list if the paper does not measure or evaluate bias.
2. `primary_bias_target`: the single primary bias target that is the main focus of the paper.
   - If the paper has a clear primary focus, use that bias category (e.g., "Religious bias", "Gender bias").
   - If the paper measures multiple biases equally without a single primary focus, or measures none, use "No Primary Bias Target".
"""

RELIGIOUS_DETAIL_PROMPT = """Analyze this academic paper and provide a deep dive on its relation to faith/religion.
Do NOT transcribe references or bibliography entries.

Return JSON matching the schema with these fields:
1. `religion_component`: "major" if religion is the paper's main focus, "minor" if religion is one component evaluated alongside other categories, or "none" if the paper does not actually analyze aspects of religion.
2. `measurement_description`: what specifically the paper measured or evaluated regarding faith/religion.
3. `religious_groups`: specific religious groups measured or mentioned (e.g., Christianity, Islam, Judaism, Buddhism, Hinduism, Atheism, Mormon, etc.).
4. `models_tested`: specific Large Language Models evaluated in this paper (e.g., GPT-4o, Llama-3.1-8B-Instruct, Claude 3.5 Sonnet, Gemini 2.5 Pro).
5. `languages_evaluated`: languages evaluated in this paper (default to ["English"] if not explicitly stated).
6. `response_type`: list of strings using ONLY "short" (multiple choice / short answers), "long" (open-ended text generation), or "other". Multiple values allowed if both are evaluated.
7. `base_benchmarks`: existing benchmarks this paper builds on, extends, or evaluates with (e.g., BBQ, StereoSet, CrowS-Pairs, BOLD). Empty list if none.
8. `continuous_testing`: true only if the paper indicates an ongoing/continuously updated evaluation or benchmark, otherwise false.
9. `findings`: concise summary of the paper's key empirical findings related to religion.
"""

RELIGION_HTTP_TIMEOUT_MS = 180_000


def select_pending_religion_candidates(
    conn: sqlite3.Connection,
    *,
    threshold: float = 0.40,
    limit: int | None = None,
    since: str | None = None,
    until: str | None = None,
) -> list[sqlite3.Row]:
    """Select papers routed via orthogonal is_llm_bias_ethics_religion flag (including uses_only)."""
    sql = """
        SELECT DISTINCT p.arxiv_id, p.title, p.published_date, p.latest_version_seen, p.gcs_pdf_uri
        FROM papers p
        INNER JOIN triage_assessments t
            ON t.arxiv_id = p.arxiv_id
           AND t.rubric_id = 'ai_benchmark_triage'
           AND t.question_id = 'is_llm_bias_ethics_religion'
           AND t.probability >= ?
        LEFT JOIN paper_stage_status s
            ON s.arxiv_id = p.arxiv_id AND s.stage = 'religion_extract'
        WHERE p.is_withdrawn = 0
          AND (s.status IS NULL OR s.status IN ('pending', 'failed_transient'))
          AND (
              s.status IN ('pending', 'failed_transient')
              OR NOT EXISTS (
                  SELECT 1 FROM paper_stage_status sbt
                  WHERE sbt.arxiv_id = p.arxiv_id
                    AND sbt.stage = 'religion_bias_targets'
                    AND sbt.status = 'done'
              )
          )
          AND (
              s.status IN ('pending', 'failed_transient')
              OR NOT EXISTS (
                  SELECT 1 FROM paper_bias_targets bt
                  WHERE bt.arxiv_id = p.arxiv_id
              )
          )
    """
    params: list[Any] = [threshold]
    if since is not None or until is not None:
        sql += " AND p.published_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*'"
    if since is not None:
        sql += " AND p.published_date >= ?"
        params.append(since)
    if until is not None:
        sql += " AND p.published_date <= ?"
        params.append(until)
    sql += " ORDER BY p.published_date DESC, p.arxiv_id DESC"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    return conn.execute(sql, params).fetchall()


def _call_religion_gemini_with_retries(
    sdk: Any,
    *,
    model: str,
    contents: list[Any],
    schema: type[Any],
    stage: str,
    arxiv_id: str,
    run_id: str | None,
    writer: SingleWriterQueue,
    max_retries: int = 4,
) -> tuple[Any, int, int, float]:
    model_id = _normalize_model_name(model)
    in_rate, out_rate = flash_cost_rates_per_1m(model_id)
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        t0 = time.monotonic()
        try:
            resp = sdk.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.0,
                ),
            )
            latency_ms = int((time.monotonic() - t0) * 1000)
            parsed = schema.model_validate_json((resp.text or "").strip())
            usage = getattr(resp, "usage_metadata", None)
            in_tok = int(getattr(usage, "prompt_token_count", 0) or 0)
            out_tok = int(getattr(usage, "candidates_token_count", 0) or 0) + int(
                getattr(usage, "thoughts_token_count", 0) or 0
            )
            cost_usd = (in_tok / 1_000_000.0) * in_rate + (out_tok / 1_000_000.0) * out_rate
            writer.submit_sql(
                """
                INSERT INTO api_call_logs (
                    run_id, stage, endpoint, model, arxiv_id,
                    prompt_tokens, output_tokens, estimated_cost_usd,
                    latency_ms, http_status, created_at
                ) VALUES (?, ?, 'generateContent', ?, ?, ?, ?, ?, ?, 200, ?)
                """,
                (
                    run_id,
                    stage,
                    model_id,
                    arxiv_id,
                    in_tok,
                    out_tok,
                    cost_usd,
                    latency_ms,
                    datetime.now(UTC).isoformat(),
                ),
            )
            return parsed, in_tok, out_tok, cost_usd
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            status = _extract_status_code(exc)
            latency_ms = int((time.monotonic() - t0) * 1000)
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
                    stage,
                    model_id,
                    arxiv_id,
                    latency_ms,
                    status,
                    datetime.now(UTC).isoformat(),
                ),
            )
            if (
                not is_daily_quota_error(exc, status)
                and _is_retryable_network_error(exc, status)
                and attempt + 1 < max_retries
            ):
                time.sleep(min(25.0, 2.0 * (2**attempt)) + random.uniform(0.3, 1.5))
                continue
            raise
    assert last_exc is not None
    raise last_exc


def extract_religion_papers(
    conn: sqlite3.Connection,
    writer: SingleWriterQueue,
    settings: Settings,
    storage: PdfStorageManager,
    *,
    threshold: float = 0.40,
    limit: int | None = None,
    since: str | None = None,
    until: str | None = None,
    workers: int = 8,
    run_id: str | None = None,
    client: Any | None = None,
) -> dict[str, Any]:
    """Extract bias targets and religious-bias details for orthogonal religion-routed papers."""
    logger = logging.getLogger("arxiv_bench")
    candidates = select_pending_religion_candidates(
        conn, threshold=threshold, limit=limit, since=since, until=until
    )
    if not candidates:
        return {
            "attempted": 0,
            "bias_extracted": 0,
            "religion_extracted": 0,
            "religion_major_minor": 0,
            "withdrawn": 0,
            "failed": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "estimated_cost_usd": 0.0,
            "new_religion_arxiv_ids": [],
            "sample_errors": [],
        }

    tls = threading.local()

    def _get_sdk() -> Any:
        if client is not None:
            return client
        sdk_local = getattr(tls, "sdk", None)
        if sdk_local is None:
            sdk_local = genai.Client(
                api_key=settings.google_api_key,
                http_options={"timeout": RELIGION_HTTP_TIMEOUT_MS},
            )
            tls.sdk = sdk_local
        return sdk_local

    def _process_one(row: sqlite3.Row) -> dict[str, Any]:
        arxiv_id = str(row["arxiv_id"])
        staged = None
        uploaded = None
        sdk = _get_sdk()
        in_total = 0
        out_total = 0
        cost_total = 0.0
        rel_extracted = False
        rel_comp = ""
        try:
            staged = storage.stage_pdf(
                arxiv_id,
                gcs_pdf_uri=row["gcs_pdf_uri"],
                version=row["latest_version_seen"],
            )
            size_bytes = staged.local_path.stat().st_size
            if size_bytes < INLINE_PDF_MAX_BYTES:
                pdf_input: Any = types.Part.from_bytes(
                    data=staged.local_path.read_bytes(),
                    mime_type="application/pdf",
                )
            else:
                uploaded = sdk.files.upload(file=str(staged.local_path))
                pdf_input = uploaded

            # Step A: Bias targets
            bt_data, bt_in, bt_out, bt_cost = _call_religion_gemini_with_retries(
                sdk,
                model=settings.religion_model,
                contents=[pdf_input, BIAS_TARGETS_PROMPT],
                schema=BiasTargetsExtraction,
                stage="religion_bias_targets",
                arxiv_id=arxiv_id,
                run_id=run_id,
                writer=writer,
            )
            in_total += bt_in
            out_total += bt_out
            cost_total += bt_cost

            primary_norm = (
                normalize_bias_target(bt_data.primary_bias_target)
                if bt_data.primary_bias_target
                else ""
            )
            raw_targets = [entry.target for entry in bt_data.bias_targets]
            now_bt = datetime.now(UTC).isoformat()

            def _write_bias(
                cur: sqlite3.Cursor,
                aid: str = arxiv_id,
                data: BiasTargetsExtraction = bt_data,
                pnorm: str = primary_norm,
                ts: str = now_bt,
            ) -> None:
                cur.execute("DELETE FROM paper_bias_targets WHERE arxiv_id = ?", (aid,))
                for entry in data.bias_targets:
                    t_norm = normalize_bias_target(entry.target)
                    is_prim = 1 if pnorm and t_norm.lower() == pnorm.lower() else 0
                    cur.execute(
                        """
                        INSERT OR IGNORE INTO paper_bias_targets (arxiv_id, target, methodology, is_primary)
                        VALUES (?, ?, ?, ?)
                        """,
                        (aid, t_norm, entry.methodology.strip(), is_prim),
                    )
                cur.execute(
                    """
                    INSERT INTO paper_stage_status (arxiv_id, stage, status, attempt_count, run_id, updated_at)
                    VALUES (?, 'religion_bias_targets', 'done', 1, ?, ?)
                    ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                        status = 'done',
                        attempt_count = paper_stage_status.attempt_count + 1,
                        last_error_code = NULL,
                        last_error_detail = NULL,
                        run_id = excluded.run_id,
                        updated_at = excluded.updated_at
                    """,
                    (aid, run_id, ts),
                )

            writer.submit(_write_bias)

            # Step B: Deep religious-bias details (omitting bibliography transcription)
            if _has_religious_target(raw_targets, bt_data.primary_bias_target):
                rel_data, rel_in, rel_out, rel_cost = _call_religion_gemini_with_retries(
                    sdk,
                    model=settings.religion_model,
                    contents=[pdf_input, RELIGIOUS_DETAIL_PROMPT],
                    schema=ReligiousBiasDetailExtraction,
                    stage="religion_extract",
                    arxiv_id=arxiv_id,
                    run_id=run_id,
                    writer=writer,
                )
                in_total += rel_in
                out_total += rel_out
                cost_total += rel_cost
                rel_extracted = True
                rel_comp = str(rel_data.religion_component or "").lower()
                now_iso = datetime.now(UTC).isoformat()
                writer.submit_sql(
                    """
                    INSERT INTO religious_bias_details (
                        arxiv_id, religion_component, measurement_description,
                        religious_groups_json, models_tested_json, languages_json,
                        response_type_json, base_benchmarks_json, continuous_testing,
                        findings, extracted_at, run_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(arxiv_id) DO UPDATE SET
                        religion_component = excluded.religion_component,
                        measurement_description = excluded.measurement_description,
                        religious_groups_json = excluded.religious_groups_json,
                        models_tested_json = excluded.models_tested_json,
                        languages_json = excluded.languages_json,
                        response_type_json = excluded.response_type_json,
                        base_benchmarks_json = excluded.base_benchmarks_json,
                        continuous_testing = excluded.continuous_testing,
                        findings = excluded.findings,
                        extracted_at = excluded.extracted_at,
                        run_id = excluded.run_id
                    """,
                    (
                        arxiv_id,
                        rel_data.religion_component,
                        rel_data.measurement_description,
                        json.dumps(rel_data.religious_groups),
                        json.dumps(rel_data.models_tested),
                        json.dumps(rel_data.languages_evaluated),
                        json.dumps(rel_data.response_type),
                        json.dumps(rel_data.base_benchmarks),
                        1 if rel_data.continuous_testing else 0,
                        rel_data.findings,
                        now_iso,
                        run_id,
                    ),
                )

            archive = storage.archive_and_cleanup(staged, published_date=row["published_date"])
            staged = None
            writer.submit_sql(
                """
                UPDATE papers
                SET gcs_pdf_uri = COALESCE(?, gcs_pdf_uri),
                    pdf_sha256 = COALESCE(?, pdf_sha256),
                    pdf_sync_status = ?
                WHERE arxiv_id = ?
                """,
                (archive.gcs_pdf_uri, archive.pdf_sha256, archive.pdf_sync_status, arxiv_id),
            )
            writer.submit_sql(
                """
                INSERT INTO paper_stage_status (arxiv_id, stage, status, attempt_count, run_id, updated_at)
                VALUES (?, 'religion_extract', 'done', 1, ?, ?)
                ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                    status = 'done',
                    attempt_count = paper_stage_status.attempt_count + 1,
                    last_error_code = NULL,
                    last_error_detail = NULL,
                    run_id = excluded.run_id,
                    updated_at = excluded.updated_at
                """,
                (arxiv_id, run_id, datetime.now(UTC).isoformat()),
            )
            return {
                "ok": True,
                "arxiv_id": arxiv_id,
                "rel_extracted": rel_extracted,
                "rel_comp": rel_comp,
                "in_tok": in_total,
                "out_tok": out_total,
                "cost": cost_total,
            }
        except WithdrawnPaperError as exc:
            err_msg = str(exc)[:300]
            writer.submit_sql(
                """
                UPDATE papers SET is_withdrawn = 1 WHERE arxiv_id = ?
                """,
                (arxiv_id,),
            )
            writer.submit_sql(
                """
                INSERT INTO paper_stage_status (
                    arxiv_id, stage, status, attempt_count, last_error_code, last_error_detail, run_id, updated_at
                ) VALUES (?, 'religion_extract', 'failed_permanent', 1, 'withdrawn', ?, ?, ?)
                ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                    status = 'failed_permanent',
                    attempt_count = paper_stage_status.attempt_count + 1,
                    last_error_code = 'withdrawn',
                    last_error_detail = excluded.last_error_detail,
                    run_id = excluded.run_id,
                    updated_at = excluded.updated_at
                """,
                (arxiv_id, err_msg, run_id, datetime.now(UTC).isoformat()),
            )
            return {
                "ok": False,
                "withdrawn": True,
                "arxiv_id": arxiv_id,
                "error": f"{arxiv_id}: {err_msg}",
                "in_tok": in_total,
                "out_tok": out_total,
                "cost": cost_total,
            }
        except Exception as exc:  # noqa: BLE001
            err_msg = f"{type(exc).__name__}: {str(exc)[:300]}"
            writer.submit_sql(
                """
                INSERT INTO paper_stage_status (
                    arxiv_id, stage, status, attempt_count, last_error_code, last_error_detail, run_id, updated_at
                ) VALUES (?, 'religion_extract', 'failed_transient', 1, ?, ?, ?, ?)
                ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                    status = 'failed_transient',
                    attempt_count = paper_stage_status.attempt_count + 1,
                    last_error_code = excluded.last_error_code,
                    last_error_detail = excluded.last_error_detail,
                    run_id = excluded.run_id,
                    updated_at = excluded.updated_at
                """,
                (
                    arxiv_id,
                    str(_extract_status_code(exc)),
                    err_msg,
                    run_id,
                    datetime.now(UTC).isoformat(),
                ),
            )
            return {
                "ok": False,
                "withdrawn": False,
                "arxiv_id": arxiv_id,
                "error": f"{arxiv_id}: {err_msg}",
                "in_tok": in_total,
                "out_tok": out_total,
                "cost": cost_total,
            }
        finally:
            if uploaded is not None:
                try:
                    sdk.files.delete(name=uploaded.name)
                except Exception:  # noqa: BLE001
                    pass
            if staged is not None:
                storage.cleanup_staged(staged)

    stats: dict[str, Any] = {
        "attempted": 0,
        "bias_extracted": 0,
        "religion_extracted": 0,
        "religion_major_minor": 0,
        "withdrawn": 0,
        "failed": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "estimated_cost_usd": 0.0,
        "new_religion_arxiv_ids": [],
        "sample_errors": [],
    }
    t0 = time.monotonic()
    total = len(candidates)
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futs = [pool.submit(_process_one, row) for row in candidates]
        for fut in as_completed(futs):
            res = fut.result()
            stats["attempted"] += 1
            stats["total_input_tokens"] += int(res["in_tok"])
            stats["total_output_tokens"] += int(res["out_tok"])
            stats["estimated_cost_usd"] += float(res["cost"])
            if res["ok"]:
                stats["bias_extracted"] += 1
                if res["rel_extracted"]:
                    stats["religion_extracted"] += 1
                    if res["rel_comp"] in ("major", "minor"):
                        stats["religion_major_minor"] += 1
                        stats["new_religion_arxiv_ids"].append(res["arxiv_id"])
            else:
                if res.get("withdrawn"):
                    stats["withdrawn"] += 1
                else:
                    stats["failed"] += 1
                if len(stats["sample_errors"]) < 15:
                    stats["sample_errors"].append(res["error"])

            if stats["attempted"] % 25 == 0 or stats["attempted"] == total:
                prog = {
                    "event": "religion_extract_progress",
                    "run_id": run_id,
                    "done": stats["attempted"],
                    "total": total,
                    "bias_extracted": stats["bias_extracted"],
                    "religion_major_minor": stats["religion_major_minor"],
                    "failed": stats["failed"],
                    "withdrawn": stats["withdrawn"],
                    "est_cost_usd": round(stats["estimated_cost_usd"], 4),
                    "elapsed_s": round(time.monotonic() - t0, 1),
                }
                logger.info(json.dumps(prog))
                print(json.dumps(prog), file=sys.stderr, flush=True)

    writer.flush()
    stats["estimated_cost_usd"] = round(float(stats["estimated_cost_usd"]), 6)
    stats["new_religion_arxiv_ids"].sort(reverse=True)
    return stats


def generate_daily_update(
    conn: sqlite3.Connection,
    run_id: str,
    output_path: Path,
) -> int:
    """Generate daily religious-bias update strictly scoped to pipeline_runs.mode = 'daily'."""
    rows = conn.execute(
        """
        SELECT
            v.arxiv_id, v.title, v.published_date,
            v.religion_component, v.measurement_description, v.findings
        FROM v_religion_papers v
        INNER JOIN pipeline_runs pr ON pr.run_id = v.run_id
        WHERE pr.run_id = ?
          AND pr.mode = 'daily'
          AND lower(COALESCE(v.religion_component, '')) IN ('major', 'minor')
        ORDER BY v.arxiv_id DESC
        """,
        (run_id,),
    ).fetchall()

    if not rows:
        return 0

    lines = [
        f"# Analysis Update - {datetime.now(UTC).strftime('%Y-%m-%d %H:%M')}\n",
        f"**New papers analyzed:** {len(rows)}\n",
    ]
    for r in rows:
        title = r["title"] or "Unknown Title"
        pub_date = r["published_date"] or "Unknown Date"
        url = get_arxiv_url(r["arxiv_id"])
        combined = f"{r['measurement_description'] or ''} {r['findings'] or ''}".strip()
        mormon_tag = " #Mormon" if check_mormon_mention(combined + " " + title) else ""
        focus_tag = (
            " #ReligionFocus" if str(r["religion_component"] or "").lower() == "major" else ""
        )
        lines.append(f"## {title}{mormon_tag}{focus_tag}\n")
        lines.append(f"[{url}]({url})\n")
        lines.append(f"**Date:** {pub_date}\n")
        lines.append(f"{combined}\n")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(rows)


def generate_full_reports(
    conn: sqlite3.Connection,
    output_dir: Path,
) -> ReligionReportCounts:
    """Generate legacy-compatible religious-bias & LLM-bias Markdown reports directly from SQLite."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Count total LLM+bias papers (imported legacy metadata + extracted bias targets + Stage 1 orthogonal flag)
    llm_bias_count = int(
        conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT arxiv_id FROM papers
                WHERE legacy_metadata_json IS NOT NULL
                  AND json_extract(legacy_metadata_json, '$.is_llm_related') = 1
                  AND json_extract(legacy_metadata_json, '$.is_bias_related') = 1
                UNION
                SELECT arxiv_id FROM paper_bias_targets
                UNION
                SELECT arxiv_id FROM triage_assessments
                WHERE rubric_id = 'ai_benchmark_triage'
                  AND question_id = 'is_llm_bias_ethics_religion'
                  AND probability >= 0.40
            )
            """
        ).fetchone()[0]
    )

    rel_rows = conn.execute(
        """
        SELECT v.*
        FROM v_religion_papers v
        WHERE lower(COALESCE(v.religion_component, '')) IN ('major', 'minor')
        ORDER BY v.arxiv_id DESC
        """
    ).fetchall()

    primary_ids = {
        str(r["arxiv_id"])
        for r in conn.execute(
            """
            SELECT DISTINCT arxiv_id
            FROM paper_bias_targets
            WHERE is_primary = 1 AND lower(target) LIKE '%relig%'
            """
        ).fetchall()
    }

    religious_groups = Counter[str]()
    models_tested = Counter[str]()
    languages = Counter[str]()
    base_benchmarks = Counter[str]()
    response_types = Counter[str]()
    continuous_testing = Counter[str]()

    for r in rel_rows:
        for grp in json.loads(r["religious_groups_json"] or "[]"):
            if isinstance(grp, str) and grp.strip():
                religious_groups[normalize_religious_group(grp)] += 1
        for mdl in json.loads(r["models_tested_json"] or "[]"):
            if isinstance(mdl, str) and mdl.strip():
                models_tested[normalize_model_name(mdl)] += 1
        for lang in json.loads(r["languages_json"] or "[]"):
            if isinstance(lang, str) and lang.strip():
                languages[lang.strip()] += 1
        for bench in json.loads(r["base_benchmarks_json"] or "[]"):
            if isinstance(bench, str) and bench.strip():
                base_benchmarks[bench.strip()] += 1
        raw_rts = [
            rt.strip().lower()
            for rt in json.loads(r["response_type_json"] or "[]")
            if isinstance(rt, str) and rt.strip()
        ]
        has_short = "short" in raw_rts
        has_long = "long" in raw_rts
        if has_short and has_long:
            response_types["Both"] += 1
        elif has_short:
            response_types["Short"] += 1
        elif has_long:
            response_types["Long"] += 1
        elif raw_rts:
            response_types["Other"] += 1
        ct = r["continuous_testing"]
        continuous_testing["Yes" if ct else "No"] += 1

    # Indexed SQL join over paper_citations replacing the O(N^2) fuzzy reference loop
    top_refs = conn.execute(
        """
        SELECT COALESCE(pc.cited_title, pc.cited_arxiv_id, pc.cited_s2_id) AS label,
               COUNT(DISTINCT pc.citing_arxiv_id) AS cnt
        FROM paper_citations pc
        INNER JOIN religious_bias_details r ON r.arxiv_id = pc.citing_arxiv_id
        WHERE lower(COALESCE(r.religion_component, '')) IN ('major', 'minor')
        GROUP BY pc.cited_s2_id
        ORDER BY cnt DESC, label ASC
        LIMIT 100
        """
    ).fetchall()
    ref_counter = Counter({str(r["label"]): int(r["cnt"]) for r in top_refs})

    primary_papers = [r for r in rel_rows if str(r["arxiv_id"]) in primary_ids]
    primary_sorted = sorted(
        primary_papers,
        key=lambda r: (-(r["citation_count"] or 0), r["title"] or ""),
    )
    all_sorted = sorted(
        rel_rows,
        key=lambda r: (-(r["citation_count"] or 0), r["title"] or ""),
    )

    denom = len(rel_rows)
    stats_lines = [
        "# Religious Bias Papers - Statistics and Links\n",
        f"**Count of LLM-Bias papers:** {llm_bias_count}\n",
        f"**Count of papers measuring religious bias:** {len(rel_rows)}\n",
        f"**Count of papers where religious bias is the primary focus:** {len(primary_papers)}\n",
        _generate_markdown_table(
            religious_groups,
            "Religious Groups Studied (Top 25)",
            "Religious Group",
            "Count",
            limit=25,
            denominator=denom,
        ),
        _generate_markdown_table(
            models_tested, "Models Tested (Top 25)", "Model", "Count", limit=25, denominator=denom
        ),
        _generate_markdown_table(
            languages,
            "Languages Evaluated (Top 25)",
            "Language",
            "Count",
            limit=25,
            denominator=denom,
        ),
        _generate_markdown_table(
            base_benchmarks,
            "Base Benchmarks (Top 25)",
            "Benchmark",
            "Count",
            limit=25,
            denominator=denom,
        ),
        _generate_markdown_table(
            response_types, "Response Type", "Type", "Count", denominator=denom
        ),
        _generate_markdown_table(
            continuous_testing, "Continuous Testing", "Status", "Count", denominator=denom
        ),
        _generate_markdown_table(
            ref_counter, "Most Cited Papers (Top 100)", "Cited Paper", "Count", limit=100
        ),
        "## Papers Primarily Measuring Religious Bias\n",
    ]
    for r in primary_sorted:
        cites = r["citation_count"] if r["citation_count"] is not None else "N/A"
        stats_lines.append(
            f"- [{r['title'] or 'Unknown Title'}]({get_arxiv_url(r['arxiv_id'])}) (citations: {cites})"
        )
    stats_lines.append("\n## All Papers Measuring Religious Bias\n")
    for r in all_sorted:
        cites = r["citation_count"] if r["citation_count"] is not None else "N/A"
        stats_lines.append(
            f"- [{r['title'] or 'Unknown Title'}]({get_arxiv_url(r['arxiv_id'])}) (citations: {cites})"
        )
    stats_lines.append("")

    stats_path = output_dir / "Religious Bias Papers - Statistics and Links.md"
    stats_path.write_text("\n".join(stats_lines), encoding="utf-8")

    # Summaries report
    sum_lines = ["# Religious Bias Papers - Summaries\n"]
    for r in rel_rows:
        title = r["title"] or "Unknown Title"
        pub_date = r["published_date"] or "Unknown Date"
        url = get_arxiv_url(r["arxiv_id"])
        combined = f"{r['measurement_description'] or ''} {r['findings'] or ''}".strip()
        mormon_tag = " #Mormon" if check_mormon_mention(combined + " " + title) else ""
        sum_lines.append(f"## {title}{mormon_tag}\n")
        sum_lines.append(f"[{url}]({url})\n")
        sum_lines.append(f"**Date:** {pub_date}\n")
        sum_lines.append(f"{combined}\n")
        sum_lines.append("")

    summaries_path = output_dir / "Religious Bias Papers - Summaries.md"
    summaries_path.write_text("\n".join(sum_lines), encoding="utf-8")

    # LLM Bias Papers - Statistics.md
    bias_stats_path = output_dir / "LLM Bias Papers - Statistics.md"
    generate_bias_targets_analysis(conn, output_dir, stats_markdown_path=bias_stats_path)

    return ReligionReportCounts(
        llm_bias_papers=llm_bias_count,
        religion_papers=len(rel_rows),
        religion_primary_papers=len(primary_papers),
        reports_written=[str(stats_path), str(summaries_path), str(bias_stats_path)],
    )


def generate_bias_targets_analysis(
    conn: sqlite3.Connection,
    output_dir: Path,
    *,
    stats_markdown_path: Path | None = None,
) -> Path:
    """Compute bias-target frequency, focus analysis (primary or exclusive), and Sankey CSV."""
    rows = conn.execute("SELECT arxiv_id, target, is_primary FROM paper_bias_targets").fetchall()
    by_paper: dict[str, list[tuple[str, int]]] = {}
    for r in rows:
        by_paper.setdefault(str(r["arxiv_id"]), []).append(
            (normalize_bias_target(str(r["target"])), int(r["is_primary"]))
        )

    done_count = int(
        conn.execute(
            """
            SELECT COUNT(*)
            FROM paper_stage_status
            WHERE stage = 'religion_bias_targets' AND status = 'done'
            """
        ).fetchone()[0]
    )
    total_analyzed = max(done_count, len(by_paper))

    total_counter = Counter[str]()
    singleton_counter = Counter[str]()
    primary_counter = Counter[str]()
    focused_counter = Counter[str]()

    for entries in by_paper.values():
        unique_targets = {t for t, _ in entries}
        primary_targets = {t for t, is_prim in entries if is_prim}
        is_exclusive = len(unique_targets) == 1
        for t in unique_targets:
            total_counter[t] += 1
            if is_exclusive or t in primary_targets:
                focused_counter[t] += 1
        if is_exclusive:
            singleton_counter[next(iter(unique_targets))] += 1
        for t in primary_targets:
            primary_counter[t] += 1

    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = stats_markdown_path or (output_dir / "LLM Bias Papers - Statistics.md")
    denom = total_analyzed or 1
    lines = [
        "# LLM Bias Papers - Statistics\n",
        f"**Total LLM-Bias papers analyzed:** {total_analyzed}\n",
        _generate_markdown_table(
            total_counter,
            "Top 25 Bias Targets",
            "Target",
            "Count",
            limit=25,
            denominator=denom,
        ),
        _generate_markdown_table(
            focused_counter,
            "Focus Analysis (Primary or Exclusive focus)",
            "Target",
            "Count",
            limit=25,
            denominator=denom,
        ),
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    sankey_csv = output_dir / "sankey_data.csv"
    with sankey_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["target", "total_papers", "singleton_papers", "primary_papers", "focused_papers"]
        )
        for target, cnt in total_counter.most_common():
            w.writerow(
                [
                    target,
                    cnt,
                    singleton_counter[target],
                    primary_counter[target],
                    focused_counter[target],
                ]
            )

    return md_path


def generate_nonbias_religion_ethics_report(
    conn: sqlite3.Connection,
    output_path: Path,
) -> int:
    """SQLite replacement for scripts/generate_nonbias_religion_ethics_report.py."""
    tags = ("religion", "ethics", "moral_reasoning", "bias_and_fairness")
    rows = conn.execute(
        """
        SELECT arxiv_id, title, published_date, legacy_metadata_json
        FROM papers
        WHERE legacy_metadata_json IS NOT NULL
          AND json_extract(legacy_metadata_json, '$.is_llm_related') = 1
          AND COALESCE(json_extract(legacy_metadata_json, '$.is_bias_related'), 0) = 0
        ORDER BY published_date DESC, arxiv_id DESC
        """
    ).fetchall()

    matched: list[dict[str, Any]] = []
    tag_counts = Counter[str]()
    combo_counts = Counter[str]()
    for r in rows:
        meta = json.loads(r["legacy_metadata_json"])
        active = [t for t in tags if meta.get(t) is True]
        if not active:
            continue
        for t in active:
            tag_counts[t] += 1
        combo_counts[" + ".join(sorted(active))] += 1
        matched.append(
            {
                "arxiv_id": r["arxiv_id"],
                "title": r["title"] or meta.get("title") or "Unknown Title",
                "date": r["published_date"] or meta.get("date") or "Unknown Date",
                "tags": active,
                "reasoning": meta.get("reasoning") or "",
            }
        )

    lines = [
        "# Non-Bias Religion and Ethics Papers\n",
        "LLM-related papers that are **not** classified as bias-related, but are tagged with",
        "religion, ethics, moral reasoning, or bias & fairness topics.\n",
        f"**Total papers: {len(matched)}**\n",
        _generate_markdown_table(tag_counts, "Tag Distribution", "Tag", "Count"),
        _generate_markdown_table(
            combo_counts, "Tag Combinations", "Combination", "Count", limit=15, heading_level=3
        ),
    ]
    for item in matched:
        url = get_arxiv_url(item["arxiv_id"])
        lines.append(f"## {item['title']}\n")
        lines.append(f"[{url}]({url})\n")
        lines.append(f"**Date:** {item['date']}\n")
        lines.append(f"**Tags:** {', '.join(item['tags'])}\n")
        if item["reasoning"]:
            lines.append(f"{item['reasoning']}\n")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(matched)


def _classify_cs_categories(categories_json: str | None) -> tuple[bool, bool, list[str], list[str]]:
    """Return (has_cs, has_non_cs, all_cats, non_cs_cats) from categories_json."""
    if not categories_json:
        return False, False, [], []
    cats = [str(c).strip() for c in json.loads(categories_json) if str(c).strip()]
    if not cats:
        return False, False, [], []
    has_cs = any(c.startswith("cs.") for c in cats)
    non_cs = [c for c in cats if not c.startswith("cs.")]
    return has_cs, bool(non_cs), cats, non_cs


def generate_wider_net_report(conn: sqlite3.Connection, output_path: Path) -> int:
    """SQLite replacement for scripts/identify_wider_net_papers.py (zero 4.5 GB snapshot scan)."""
    # 1. Broader LLM-bias category distribution
    all_bias_rows = conn.execute(
        """
        SELECT DISTINCT p.arxiv_id, p.categories_json
        FROM papers p
        WHERE (json_extract(p.legacy_metadata_json, '$.is_llm_related') = 1
               AND json_extract(p.legacy_metadata_json, '$.is_bias_related') = 1)
           OR EXISTS (SELECT 1 FROM paper_bias_targets bt WHERE bt.arxiv_id = p.arxiv_id)
           OR EXISTS (SELECT 1 FROM religious_bias_details r WHERE r.arxiv_id = p.arxiv_id)
        """
    ).fetchall()

    a_cs_only = 0
    a_cross = 0
    a_excl_non_cs = 0
    a_missing = 0
    all_non_cs_counts = Counter[str]()
    for r in all_bias_rows:
        has_cs, has_non_cs, cats, non_cs = _classify_cs_categories(r["categories_json"])
        if not cats:
            a_missing += 1
        elif has_non_cs and not has_cs:
            a_excl_non_cs += 1
        elif has_non_cs and has_cs:
            a_cross += 1
        else:
            a_cs_only += 1
        for c in non_cs:
            all_non_cs_counts[c] += 1

    # 2. Religious-bias papers with non-CS categories
    rel_rows = conn.execute(
        """
        SELECT arxiv_id, title, published_date, categories_json,
               measurement_description, findings
        FROM v_religion_papers
        ORDER BY arxiv_id DESC
        """
    ).fetchall()

    r_excl_non_cs = 0
    r_cross = 0
    wider: list[dict[str, Any]] = []
    rel_non_cs_counts = Counter[str]()
    for r in rel_rows:
        has_cs, has_non_cs, cats, non_cs = _classify_cs_categories(r["categories_json"])
        if not has_non_cs:
            continue
        if has_cs:
            r_cross += 1
        else:
            r_excl_non_cs += 1
        for c in non_cs:
            rel_non_cs_counts[c] += 1
        wider.append(
            {
                "arxiv_id": r["arxiv_id"],
                "title": r["title"] or "Unknown Title",
                "date": r["published_date"] or "Unknown Date",
                "all_cats": " ".join(cats),
                "non_cs": non_cs,
                "combined": f"{r['measurement_description'] or ''} {r['findings'] or ''}".strip(),
            }
        )

    total_bias = len(all_bias_rows) or 1
    lines = [
        "# Picked Up with Wider Net\n",
        "Papers that include non-CS arXiv categories, indicating they were cross-listed or",
        "primarily categorized outside Computer Science.\n",
        "## All Bias-in-LLM Papers (Summary Statistics)\n",
        f"Out of **{len(all_bias_rows):,}** total bias-in-LLM papers in the pipeline:\n",
        "| Category | Count | % |",
        "|---|---:|---:|",
        f"| CS-only | {a_cs_only:,} | {a_cs_only / total_bias * 100:.1f}% |",
        f"| Cross-listed (CS + other) | {a_cross:,} | {a_cross / total_bias * 100:.1f}% |",
        f"| Exclusively non-CS | {a_excl_non_cs:,} | {a_excl_non_cs / total_bias * 100:.1f}% |",
        f"| Not in snapshot | {a_missing:,} | {a_missing / total_bias * 100:.1f}% |",
        "",
    ]
    if all_non_cs_counts:
        lines.extend(
            [
                "### Non-CS Categories Across All Bias Papers\n",
                "| Category | Count | Description |",
                "|---|---:|---|",
            ]
        )
        for cat, cnt in all_non_cs_counts.most_common():
            lines.append(f"| `{cat}` | {cnt} | {NON_CS_CAT_DESCRIPTIONS.get(cat, '')} |")
        lines.append("")

    lines.extend(
        [
            "## Religious Bias Papers with Non-CS Categories\n",
            f"**Total: {len(wider)}** out of {len(rel_rows)} religious bias papers "
            f"({r_excl_non_cs} exclusively non-CS, {r_cross} cross-listed with CS).\n",
        ]
    )
    if rel_non_cs_counts:
        lines.extend(
            [
                "### Category Breakdown\n",
                "| Category | Count | Description |",
                "|---|---:|---|",
            ]
        )
        for cat, cnt in rel_non_cs_counts.most_common():
            lines.append(f"| `{cat}` | {cnt} | {NON_CS_CAT_DESCRIPTIONS.get(cat, '')} |")
        lines.append("")

    for item in wider:
        url = get_arxiv_url(item["arxiv_id"])
        mormon_tag = " #Mormon" if check_mormon_mention(item["combined"]) else ""
        lines.append(f"## {item['title']}{mormon_tag}\n")
        lines.append(f"[{url}]({url})\n")
        lines.append(f"**Date:** {item['date']}\n")
        lines.append(f"**Categories:** {item['all_cats']}\n")
        lines.append(f"**Non-CS Categories:** {', '.join(item['non_cs'])}\n")
        lines.append(f"{item['combined']}\n")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(wider)


def verify_talk_fact_quote(
    conn: sqlite3.Connection,
    storage: PdfStorageManager,
    *,
    arxiv_id: str,
    claim_keywords: list[str],
    require_visual_pdf: bool = False,
) -> dict[str, Any]:
    """Verify a talk-fact claim against stored compressed text first, falling back to GCS PDF."""
    row = conn.execute(
        "SELECT title, published_date, compressed_text_zst, gcs_pdf_uri FROM papers WHERE arxiv_id = ?",
        (arxiv_id,),
    ).fetchone()
    if row is None:
        return {"arxiv_id": arxiv_id, "verified": False, "source": "not_found", "snippet": ""}

    stored_text = decompress_text(row["compressed_text_zst"])
    if stored_text and not require_visual_pdf:
        low = stored_text.lower()
        hits = [kw for kw in claim_keywords if kw.lower() in low]
        if hits:
            pos = low.find(hits[0].lower())
            snippet = stored_text[max(0, pos - 120) : pos + 240].strip()
            return {
                "arxiv_id": arxiv_id,
                "verified": True,
                "source": "stored_text",
                "snippet": snippet,
            }

    if not row["gcs_pdf_uri"]:
        return {"arxiv_id": arxiv_id, "verified": False, "source": "no_pdf_uri", "snippet": ""}

    staged = storage.stage_pdf(arxiv_id, gcs_pdf_uri=row["gcs_pdf_uri"])
    try:
        from arxiv_bench.pdf_storage import extract_local_text

        extracted = extract_local_text(staged.local_path)
        low = extracted.plain_text.lower()
        hits = [kw for kw in claim_keywords if kw.lower() in low]
        snippet = ""
        if hits:
            pos = low.find(hits[0].lower())
            snippet = extracted.plain_text[max(0, pos - 120) : pos + 240].strip()
        return {
            "arxiv_id": arxiv_id,
            "verified": bool(hits),
            "source": "gcs_pdf_streamed",
            "snippet": snippet,
        }
    finally:
        storage.cleanup_staged(staged)


def generate_talk_facts_summary(
    conn: sqlite3.Connection,
    storage: PdfStorageManager,
    output_path: Path,
    *,
    months: int = 24,
    limit: int = 40,
) -> int:
    """Compile recent high-impact religious-bias findings verified from SQLite text / GCS PDFs."""
    cutoff = (datetime.now(UTC) - timedelta(days=months * 30)).strftime("%Y-%m-%d")
    rows = conn.execute(
        """
        SELECT v.arxiv_id, v.title, v.published_date, v.citation_count,
               v.religion_component, v.findings, v.measurement_description
        FROM v_religion_papers v
        WHERE lower(COALESCE(v.religion_component, '')) IN ('major', 'minor')
          AND COALESCE(v.published_date, '9999-99-99') >= ?
          AND COALESCE(v.findings, '') != ''
        ORDER BY (CASE WHEN lower(v.religion_component) = 'major' THEN 0 ELSE 1 END),
                 COALESCE(v.citation_count, 0) DESC,
                 v.published_date DESC
        LIMIT ?
        """,
        (cutoff, limit),
    ).fetchall()

    lines = [
        "# Religious Bias Papers - Interesting Findings\n",
        f"**Window:** Papers since {cutoff} ({len(rows)} entries)\n",
    ]
    for r in rows:
        url = get_arxiv_url(r["arxiv_id"])
        cites = r["citation_count"] if r["citation_count"] is not None else "N/A"
        check = verify_talk_fact_quote(
            conn,
            storage,
            arxiv_id=r["arxiv_id"],
            claim_keywords=["relig", "bias"],
        )
        lines.append(f"## {r['title'] or 'Unknown Title'}\n")
        lines.append(
            f"- **Link:** [{url}]({url}) | **Date:** {r['published_date'] or 'Unknown'} | "
            f"**Citations:** {cites} | **Verification Source:** `{check['source']}`"
        )
        lines.append(f"- **Finding:** {r['findings']}\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(rows)
