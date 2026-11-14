"""Pydantic v2 extraction schemas, YAML rubric loaders, and deterministic entity normalization."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field, model_validator


class EvidenceCard(BaseModel):
    """Structured 1,000-1,500 token benchmark synthesis used by Stage 3 rubric sweeps."""

    task_design: str = Field(
        default="",
        description="Core tasks, prompt/input format, and target capabilities measured.",
    )
    dataset_construction: str = Field(
        default="",
        description="Data sources, annotation pipeline, size, splits, and licensing.",
    )
    scoring_protocol: str = Field(
        default="",
        description="Metrics, judge/verifier design, and baseline or human comparisons.",
    )
    contamination_controls: str = Field(
        default="",
        description="Leakage prevention, private splits, canary strings, or dynamic refreshes.",
    )
    author_reported_gaps: str = Field(
        default="",
        description="Author-acknowledged limitations, failure modes, and open evaluation gaps.",
    )

    def to_markdown(self) -> str:
        sections = [
            ("Task Design", self.task_design),
            ("Dataset Construction", self.dataset_construction),
            ("Scoring Protocol", self.scoring_protocol),
            ("Contamination Controls", self.contamination_controls),
            ("Author-Reported Gaps", self.author_reported_gaps),
        ]
        return "\n".join(f"### {title}\n{body.strip()}" for title, body in sections if body.strip())


class BenchmarkEntry(BaseModel):
    """A benchmark or dataset artifact introduced, extended, audited, or surveyed."""

    name: str
    role: Literal["introduced", "extended", "audited", "surveyed", "base_used"] = "introduced"
    url: str | None = None
    base_benchmarks: list[str] = Field(default_factory=list)


class BenchmarkExtraction(BaseModel):
    """Strict Stage 2 Gemini Flash extraction contract for qualifying AI benchmark papers."""

    contribution_type: Literal[
        "introduces",
        "extends",
        "audits_critiques",
        "surveys",
        "uses_only",
        "unrelated",
    ]
    benchmarks: list[BenchmarkEntry] = Field(default_factory=list)
    dataset_urls: list[str] = Field(default_factory=list)
    modalities: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    tasks: list[str] = Field(default_factory=list)
    evaluation_methods: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    models_tested: list[str] = Field(default_factory=list)
    base_benchmarks: list[str] = Field(default_factory=list)
    continuous_testing: bool = False
    stated_limitations: str = ""
    evidence_card: EvidenceCard = Field(default_factory=EvidenceCard)


class BiasTargetEntry(BaseModel):
    """Single demographic/social bias target and measurement methodology."""

    target: str
    methodology: str = ""


class BiasTargetsExtraction(BaseModel):
    """Religious-bias module Stage 3 structured output."""

    bias_targets: list[BiasTargetEntry] = Field(default_factory=list)
    primary_bias_target: str = ""


class ReligiousBiasDetailExtraction(BaseModel):
    """Religious-bias module Stage 4 structured output (omits raw bibliography transcription)."""

    religion_component: Literal["major", "minor", "none"] = "none"
    measurement_description: str = ""
    religious_groups: list[str] = Field(default_factory=list)
    models_tested: list[str] = Field(default_factory=list)
    languages_evaluated: list[str] = Field(default_factory=list)
    response_type: list[str] = Field(default_factory=list)
    base_benchmarks: list[str] = Field(default_factory=list)
    continuous_testing: bool = False
    findings: str = ""


class RubricQuestion(BaseModel):
    """Single declarative question inside a gemini-decision-1 YAML rubric pack."""

    id: str
    question_type: Literal["yes_no", "multiple_choice", "score"]
    instructions: str
    threshold: float = 0.50
    true_description: str | None = None
    false_description: str | None = None
    choices: dict[str, str] = Field(default_factory=dict)
    score_levels: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_question_shape(self) -> RubricQuestion:
        if self.question_type == "multiple_choice" and len(self.choices) < 2:
            raise ValueError(f"Question '{self.id}' requires at least 2 choices.")
        if self.question_type == "score" and len(self.score_levels) < 2:
            raise ValueError(f"Question '{self.id}' requires at least 2 score_levels.")
        return self

    def to_decision_param(self) -> dict[str, object]:
        """Serialize question to google-genai client.decisions.create question payload."""
        if self.question_type == "yes_no":
            payload: dict[str, object] = {
                "type": "noul",
                "instructions": self.instructions.strip(),
            }
            criteria: dict[str, str] = {}
            if self.true_description:
                criteria["true_description"] = self.true_description.strip()
            if self.false_description:
                criteria["false_description"] = self.false_description.strip()
            if criteria:
                payload["criteria"] = criteria
            return payload
        if self.question_type == "multiple_choice":
            return {
                "type": "choice",
                "instructions": self.instructions.strip(),
                "criteria": {k.strip(): v.strip() for k, v in self.choices.items()},
            }
        return {
            "type": "score",
            "instructions": self.instructions.strip(),
            "criteria": [lvl.strip() for lvl in self.score_levels],
        }


class RubricPack(BaseModel):
    """Declarative YAML rubric pack for Stage 1 triage or Stage 3 gap sweeps."""

    rubric_id: str
    rubric_version: str
    model: str = "models/gemini-decision-1"
    description: str = ""
    questions: list[RubricQuestion]

    @model_validator(mode="after")
    def _validate_unique_ids(self) -> RubricPack:
        if not self.questions:
            raise ValueError("RubricPack must contain at least one question.")
        seen: set[str] = set()
        for q in self.questions:
            if q.id in seen:
                raise ValueError(f"Duplicate question id '{q.id}' in rubric '{self.rubric_id}'.")
            seen.add(q.id)
        return self

    def threshold_for(self, question_id: str, default: float = 0.50) -> float:
        for q in self.questions:
            if q.id == question_id:
                return q.threshold
        return default


def load_rubric_yaml(path: Path) -> RubricPack:
    """Parse and validate a declarative YAML rubric pack."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Rubric YAML at '{path}' must decode to a mapping.")
    return RubricPack.model_validate(raw)


_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_MULTI_DASH_RE = re.compile(r"-{2,}")


def normalize_entity_slug(raw_name: str) -> str:
    """Compute a deterministic slug preserving distinguishing variant suffixes.

    Examples:
    - 'SWE-bench' -> 'swe-bench'
    - 'SWE-bench Verified' -> 'swe-bench-verified'
    - 'MMLU-Pro' -> 'mmlu-pro'
    - 'GPT-4o (2024-08-06)' -> 'gpt-4o-2024-08-06'
    """
    text = raw_name.strip().lower()
    text = text.replace("+", "plus")
    slug = _NON_ALNUM_RE.sub("-", text)
    slug = _MULTI_DASH_RE.sub("-", slug).strip("-")
    return slug


def normalize_repo_url(url: str | None) -> str | None:
    """Canonicalize GitHub, HuggingFace, or project URLs for exact entity resolution."""
    if not url:
        return None
    raw = url.strip()
    if not raw:
        return None
    if "://" not in raw:
        raw = "https://" + raw
    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if not host:
        return None

    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]

    parts = [p for p in path.split("/") if p]
    if host == "github.com" and len(parts) >= 2:
        # Collapse /owner/repo/tree/main/... to github.com/owner/repo
        return f"github.com/{parts[0].lower()}/{parts[1].lower()}"
    if host == "huggingface.co" and len(parts) >= 2:
        if parts[0].lower() in {"datasets", "spaces"} and len(parts) >= 3:
            return f"huggingface.co/{parts[0].lower()}/{parts[1].lower()}/{parts[2].lower()}"
        return f"huggingface.co/{parts[0].lower()}/{parts[1].lower()}"

    normalized_path = "/".join(parts).lower()
    return f"{host}/{normalized_path}" if normalized_path else host
