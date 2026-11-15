"""Pydantic v2 extraction schemas, YAML rubric loaders, and deterministic entity normalization."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Literal, get_args
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

ModalityTag = Literal[
    "text-llm",
    "vision",
    "video",
    "audio-speech",
    "multimodal",
    "3d-spatial",
    "code-software",
    "tabular-timeseries",
    "agent-tool-use",
    "robotics-embodied",
    "scientific-signals",
    "other-emergent",
]

DomainTag = Literal[
    "general-reasoning",
    "nlp-language",
    "computer-vision",
    "software-engineering",
    "math-formal",
    "agentic-systems",
    "robotics-autonomous",
    "speech-music-audio",
    "medical-healthcare",
    "biology-chemistry-materials",
    "physics-earth-climate",
    "science-general",
    "finance-economics",
    "legal-governance",
    "education-assessment",
    "safety-alignment-ethics",
    "cybersecurity",
    "social-humanities-media",
    "industrial-engineering",
    "other",
]

CONTROLLED_MODALITIES: tuple[str, ...] = get_args(ModalityTag)
CONTROLLED_DOMAINS: tuple[str, ...] = get_args(DomainTag)
_CONTROLLED_MODALITY_SET = frozenset(CONTROLLED_MODALITIES)
_CONTROLLED_DOMAIN_SET = frozenset(CONTROLLED_DOMAINS)

_MODALITY_SYNONYMS: dict[str, ModalityTag] = {
    "text": "text-llm",
    "nlp": "text-llm",
    "llm": "text-llm",
    "language": "text-llm",
    "document": "text-llm",
    "documents": "text-llm",
    "image": "vision",
    "images": "vision",
    "visual": "vision",
    "ocr": "vision",
    "computer-vision": "vision",
    "videos": "video",
    "audio": "audio-speech",
    "speech": "audio-speech",
    "voice": "audio-speech",
    "music": "audio-speech",
    "sound": "audio-speech",
    "cross-modal": "multimodal",
    "vision-language": "multimodal",
    "vlm": "multimodal",
    "audio-visual": "multimodal",
    "omni": "multimodal",
    "3d": "3d-spatial",
    "3d-vision": "3d-spatial",
    "point-cloud": "3d-spatial",
    "point-clouds": "3d-spatial",
    "3d-point-clouds": "3d-spatial",
    "3d-mesh": "3d-spatial",
    "spatial": "3d-spatial",
    "code": "code-software",
    "software": "code-software",
    "programming": "code-software",
    "tabular": "tabular-timeseries",
    "time-series": "tabular-timeseries",
    "timeseries": "tabular-timeseries",
    "structured": "tabular-timeseries",
    "sql": "tabular-timeseries",
    "graph": "tabular-timeseries",
    "graphs": "tabular-timeseries",
    "agent": "agent-tool-use",
    "agents": "agent-tool-use",
    "tool-use": "agent-tool-use",
    "gui": "agent-tool-use",
    "web": "agent-tool-use",
    "robotics": "robotics-embodied",
    "robot": "robotics-embodied",
    "embodied": "robotics-embodied",
    "scientific-medical": "scientific-signals",
    "sensor": "scientific-signals",
    "sensors": "scientific-signals",
    "sensor-data": "scientific-signals",
    "molecular": "scientific-signals",
    "biomedical": "scientific-signals",
    "other": "other-emergent",
}

_MODALITY_KEYWORD_RULES: tuple[tuple[tuple[str, ...], ModalityTag], ...] = (
    (("3d", "point-cloud", "mesh", "voxel", "lidar", "nerf", "spatial"), "3d-spatial"),
    (("video", "temporal-visual"), "video"),
    (("audio", "speech", "voice", "music", "acoustic"), "audio-speech"),
    (("multimodal", "cross-modal", "vision-language", "audio-visual", "omni"), "multimodal"),
    (("robot", "embodied", "manipulation", "navigation", "uav", "driving"), "robotics-embodied"),
    (("agent", "tool", "browser", "gui", "os-control"), "agent-tool-use"),
    (("code", "software", "program", "verilog", "formal-proof"), "code-software"),
    (
        ("tabular", "time-series", "timeseries", "forecast", "database", "sql", "graph"),
        "tabular-timeseries",
    ),
    (
        (
            "sensor",
            "signal",
            "impedance",
            "tomography",
            "eeg",
            "ecg",
            "mri",
            "molecular",
            "protein",
            "genom",
            "spectra",
        ),
        "scientific-signals",
    ),
    (("image", "vision", "visual", "ocr", "photo", "radiolog"), "vision"),
    (("text", "language", "nlp", "llm", "dialog", "document"), "text-llm"),
)

_DOMAIN_SYNONYMS: dict[str, DomainTag] = {
    "general": "general-reasoning",
    "general-knowledge": "general-reasoning",
    "reasoning": "general-reasoning",
    "commonsense": "general-reasoning",
    "nlp": "nlp-language",
    "natural-language-processing": "nlp-language",
    "language": "nlp-language",
    "information-retrieval": "nlp-language",
    "vision": "computer-vision",
    "cv": "computer-vision",
    "software": "software-engineering",
    "coding": "software-engineering",
    "code": "software-engineering",
    "programming": "software-engineering",
    "machine-learning-engineering": "software-engineering",
    "math": "math-formal",
    "mathematics": "math-formal",
    "theorem-proving": "math-formal",
    "agents": "agentic-systems",
    "agent": "agentic-systems",
    "robotics": "robotics-autonomous",
    "autonomous-driving": "robotics-autonomous",
    "human-robot-interaction": "robotics-autonomous",
    "human-robot-interaction-hri": "robotics-autonomous",
    "audio": "speech-music-audio",
    "speech": "speech-music-audio",
    "music": "speech-music-audio",
    "medical": "medical-healthcare",
    "medicine": "medical-healthcare",
    "healthcare": "medical-healthcare",
    "clinical": "medical-healthcare",
    "biomedical": "medical-healthcare",
    "biomedical-imaging": "medical-healthcare",
    "biology": "biology-chemistry-materials",
    "chemistry": "biology-chemistry-materials",
    "materials": "biology-chemistry-materials",
    "life-sciences": "biology-chemistry-materials",
    "physics": "physics-earth-climate",
    "astronomy": "physics-earth-climate",
    "climate": "physics-earth-climate",
    "geospatial": "physics-earth-climate",
    "geospatial-reasoning": "physics-earth-climate",
    "inverse-problems": "physics-earth-climate",
    "science": "science-general",
    "scientific-computing": "science-general",
    "computer-science": "science-general",
    "finance": "finance-economics",
    "economics": "finance-economics",
    "insurance": "finance-economics",
    "legal": "legal-governance",
    "law": "legal-governance",
    "governance": "legal-governance",
    "policy": "legal-governance",
    "education": "education-assessment",
    "assessment": "education-assessment",
    "safety": "safety-alignment-ethics",
    "alignment": "safety-alignment-ethics",
    "ethics": "safety-alignment-ethics",
    "fairness": "safety-alignment-ethics",
    "bias": "safety-alignment-ethics",
    "security": "cybersecurity",
    "social": "social-humanities-media",
    "social-media": "social-humanities-media",
    "affective-computing": "social-humanities-media",
    "humanities": "social-humanities-media",
    "industrial": "industrial-engineering",
    "engineering": "industrial-engineering",
    "traffic-monitoring": "industrial-engineering",
    "transportation": "industrial-engineering",
}

_DOMAIN_KEYWORD_RULES: tuple[tuple[tuple[str, ...], DomainTag], ...] = (
    (
        ("medical", "medic", "health", "clinic", "biomed", "radiol", "pathol", "patient"),
        "medical-healthcare",
    ),
    (
        ("biolog", "chem", "molecul", "protein", "genom", "drug", "material", "life-science"),
        "biology-chemistry-materials",
    ),
    (
        (
            "physic",
            "astro",
            "climat",
            "weather",
            "geospat",
            "earth",
            "remote-sens",
            "inverse-problem",
        ),
        "physics-earth-climate",
    ),
    (
        ("robot", "autonom", "driving", "uav", "drone", "human-robot", "embodied", "manipul"),
        "robotics-autonomous",
    ),
    (("agent", "tool-use", "browser", "workflow", "multi-agent"), "agentic-systems"),
    (
        (
            "software",
            "coding",
            "code",
            "program",
            "devops",
            "ml-engineer",
            "machine-learning-engineer",
        ),
        "software-engineering",
    ),
    (("math", "theorem", "formal-verif", "algebra", "geometry"), "math-formal"),
    (("cyber", "secur", "vulnerab", "malware", "cryptog", "exploit"), "cybersecurity"),
    (
        (
            "safety",
            "align",
            "ethic",
            "fairness",
            "bias",
            "red-team",
            "privacy",
            "trustworth",
            "toxic",
            "religio",
        ),
        "safety-alignment-ethics",
    ),
    (("legal", "law", "contract", "regulat", "govern", "policy"), "legal-governance"),
    (("financ", "econom", "insur", "market", "account", "trading", "bank"), "finance-economics"),
    (("educat", "tutor", "exam", "pedagog", "student", "learn"), "education-assessment"),
    (("speech", "audio", "music", "acoustic", "voice"), "speech-music-audio"),
    (("vision", "image", "video", "ocr", "visual", "3d"), "computer-vision"),
    (("nlp", "language", "translat", "summar", "retriev", "dialogue", "text"), "nlp-language"),
    (
        (
            "social",
            "affective",
            "emotion",
            "psycholog",
            "humanit",
            "media",
            "news",
            "recommend",
            "cultur",
        ),
        "social-humanities-media",
    ),
    (
        (
            "industr",
            "manufactur",
            "traffic",
            "transport",
            "energy",
            "power",
            "telecom",
            "hardware",
            "iot",
        ),
        "industrial-engineering",
    ),
    (("scien", "research", "comput"), "science-general"),
    (("general", "reason", "commonsense", "knowledge"), "general-reasoning"),
)


def normalize_modality(raw: str) -> ModalityTag | None:
    """Map a raw modality label onto the controlled 12-tag ModalityTag vocabulary."""
    slug = normalize_entity_slug(raw)
    if not slug:
        return None
    if slug in _CONTROLLED_MODALITY_SET:
        return slug  # type: ignore[return-value]
    if slug in _MODALITY_SYNONYMS:
        return _MODALITY_SYNONYMS[slug]
    for keywords, target in _MODALITY_KEYWORD_RULES:
        if any(kw in slug for kw in keywords):
            return target
    return "other-emergent"


def normalize_domain(raw: str) -> DomainTag | None:
    """Map a raw domain label onto the controlled 20-tag DomainTag vocabulary."""
    slug = normalize_entity_slug(raw)
    if not slug:
        return None
    if slug in _CONTROLLED_DOMAIN_SET:
        return slug  # type: ignore[return-value]
    if slug in _DOMAIN_SYNONYMS:
        return _DOMAIN_SYNONYMS[slug]
    for keywords, target in _DOMAIN_KEYWORD_RULES:
        if any(kw in slug for kw in keywords):
            return target
    return "other"


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
    modalities: list[ModalityTag] = Field(
        default_factory=list,
        description=(
            "1-3 controlled AI modalities targeted by the benchmark "
            "(choose only from the ModalityTag enum)."
        ),
    )
    domains: list[DomainTag] = Field(
        default_factory=list,
        description=(
            "1-3 controlled top-level application domains targeted by the benchmark "
            "(choose only from the DomainTag enum; put finer sub-domains in tasks)."
        ),
    )
    tasks: list[str] = Field(default_factory=list)
    evaluation_methods: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    models_tested: list[str] = Field(default_factory=list)
    base_benchmarks: list[str] = Field(default_factory=list)
    continuous_testing: bool = False
    stated_limitations: str = ""
    evidence_card: EvidenceCard = Field(default_factory=EvidenceCard)

    @field_validator("modalities", mode="before")
    @classmethod
    def _normalize_modalities(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return value
        out: list[ModalityTag] = []
        seen: set[str] = set()
        for item in value:
            if not isinstance(item, str):
                continue
            mapped = normalize_modality(item)
            if mapped and mapped not in seen:
                seen.add(mapped)
                out.append(mapped)
        return out

    @field_validator("domains", mode="before")
    @classmethod
    def _normalize_domains(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return value
        out: list[DomainTag] = []
        seen: set[str] = set()
        for item in value:
            if not isinstance(item, str):
                continue
            mapped = normalize_domain(item)
            if mapped and mapped not in seen:
                seen.add(mapped)
                out.append(mapped)
        return out


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
