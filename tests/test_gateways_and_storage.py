"""Unit tests for DecisionClient, ExtractionClient, PdfStorageManager, Entity Resolution, and S2Client."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from arxiv_bench.config import Settings
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.decision_client import (
    DecisionClient,
    compute_shannon_entropy,
    trim_for_decision_context,
)
from arxiv_bench.extract_client import (
    ExtractionClient,
    resolve_and_upsert_entity,
)
from arxiv_bench.pdf_storage import (
    PdfStorageManager,
    StagingQuotaError,
    WithdrawnPaperError,
    extract_local_text,
    strip_bibliography,
)
from arxiv_bench.query import merge_entity_aliases
from arxiv_bench.s2_client import SemanticScholarClient
from arxiv_bench.schemas import BenchmarkExtraction, load_rubric_yaml
from tests.conftest import FakeGCSBucket, FakeGCSClient, seed_paper


def test_decision_client_sdk_and_truncation_guard(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    seed_paper(db_conn, "2606.00001", title="ClinicalBench", abstract="New clinical benchmark.")
    rubric = load_rubric_yaml(tmp_settings.triage_rubric_path)

    captured: list[dict[str, Any]] = []

    class _FakeDecisions:
        def create(self, **kwargs: Any) -> Any:
            captured.append(kwargs)
            return SimpleNamespace(
                answers={
                    "is_benchmark_contribution": {"type": "noul", "noul": 0.92, "confidence": 0.92},
                    "contribution_type": {
                        "type": "choice",
                        "choice": "introduces",
                        "confidence": 0.88,
                        "probabilities": {"introduces": 0.88, "extends": 0.08, "uses_only": 0.04},
                    },
                    "primary_modality": {
                        "type": "choice",
                        "choice": "scientific_medical",
                        "confidence": 0.91,
                        "probabilities": {"scientific_medical": 0.91, "other_emergent": 0.09},
                    },
                    "is_llm_bias_ethics_religion": {
                        "type": "noul",
                        "noul": 0.05,
                        "confidence": 0.95,
                    },
                },
                usage=SimpleNamespace(total_input_tokens=680, total_output_tokens=0),
            )

    fake_sdk = SimpleNamespace(decisions=_FakeDecisions())
    dc = DecisionClient(tmp_settings, client=fake_sdk)

    with SingleWriterQueue(tmp_settings.db_path) as writer:
        out = dc.score_abstract(
            arxiv_id="2606.00001",
            paper_version=1,
            title="ClinicalBench",
            abstract="New clinical benchmark.",
            categories=["cs.AI"],
            rubric_pack=rubric,
            writer=writer,
            run_id="r1",
        )
        writer.flush()

    assert dc.transport_used == "sdk"
    assert len(captured) == 1
    assert captured[0]["model"] == "models/gemini-decision-1"
    assert out.output_tokens == 0
    assert out.input_tokens == 680

    rows = db_conn.execute(
        "SELECT question_id, choice_or_bool, probability FROM triage_assessments WHERE arxiv_id = '2606.00001'"
    ).fetchall()
    assert len(rows) == 4

    # Context truncation guard (>200k tokens = >800k chars)
    huge_text = "word " * 250_000
    trimmed, was_trunc = trim_for_decision_context(huge_text)
    assert was_trunc is True
    assert "[TRUNCATED_FOR_DECISION_CONTEXT_LIMIT]" in trimmed
    assert compute_shannon_entropy({"a": 0.5, "b": 0.5}) == pytest.approx(1.0, abs=1e-4)

    # Stage 3 score_rubric_pack records truncated_input=1
    gap_rubric = load_rubric_yaml(tmp_settings.repo_root / "rubrics" / "gap_analysis_core_v1.yaml")
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        dc.score_rubric_pack(
            arxiv_id="2606.00001",
            title="ClinicalBench",
            abstract="Abstract",
            evidence_card="Card",
            body_text=huge_text,
            rubric_pack=gap_rubric,
            writer=writer,
            run_id="r1",
        )
        writer.flush()
    ds = db_conn.execute(
        "SELECT truncated_input FROM decision_scores WHERE arxiv_id = '2606.00001'"
    ).fetchone()
    assert ds is not None and int(ds["truncated_input"]) == 1


def test_extraction_inline_vs_files_api_orphan_sweep_and_quarantine(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    fake_gcs: FakeGCSClient,
    sample_pdf_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_paper(db_conn, "2606.10001", title="SWE-bench Verified")
    valid_payload = BenchmarkExtraction(
        contribution_type="extends",
        benchmarks=[
            {
                "name": "SWE-bench Verified",
                "role": "extended",
                "url": "https://github.com/SWE-bench/SWE-bench.git",
                "base_benchmarks": ["SWE-bench"],
            }
        ],
        modalities=["code_software"],
        domains=["software_engineering"],
        tasks=["bug_fixing"],
        models_tested=["Claude 3.5 Sonnet"],
        stated_limitations="Python only",
    ).model_dump_json()

    deleted_files: list[str] = []
    uploaded_files: list[str] = []
    mode_state = {"response_text": valid_payload}

    class _FakeFiles:
        def list(self) -> list[Any]:
            return [
                SimpleNamespace(
                    name="files/stale-1",
                    create_time=datetime.now(UTC) - timedelta(hours=5),
                ),
                SimpleNamespace(
                    name="files/fresh-1",
                    create_time=datetime.now(UTC) - timedelta(minutes=5),
                ),
            ]

        def upload(self, file: str) -> Any:
            uploaded_files.append(file)
            return SimpleNamespace(name="files/uploaded-big", state=SimpleNamespace(name="ACTIVE"))

        def delete(self, name: str) -> None:
            deleted_files.append(name)

    class _FakeModels:
        def generate_content(self, **kwargs: Any) -> Any:
            return SimpleNamespace(
                text=mode_state["response_text"],
                usage_metadata=SimpleNamespace(prompt_token_count=1000, candidates_token_count=300),
            )

    fake_sdk = SimpleNamespace(files=_FakeFiles(), models=_FakeModels())
    storage = PdfStorageManager(tmp_settings, gcs_client=fake_gcs)
    extractor = ExtractionClient(tmp_settings, storage, client=fake_sdk, max_retries=1)

    # 1. Orphan file sweeper deletes only >2h stale files
    swept = extractor.sweep_orphan_files(max_age_hours=2.0)
    assert swept == 1
    assert deleted_files == ["files/stale-1"]

    # 2. Small PDF (<20 MB) uses inline Part.from_bytes (no files.upload!)
    parsed, err = extractor.extract_from_pdf(sample_pdf_path, arxiv_id="2606.10001")
    assert err is None and parsed is not None
    assert parsed.contribution_type == "extends"
    assert uploaded_files == []

    # 3. Large PDF (>= threshold) uses files.upload and ALWAYS calls files.delete in finally
    import arxiv_bench.extract_client as ec_mod

    monkeypatch.setattr(ec_mod, "INLINE_PDF_MAX_BYTES", 10)
    parsed2, err2 = extractor.extract_from_pdf(sample_pdf_path, arxiv_id="2606.10001")
    assert err2 is None and parsed2 is not None
    assert len(uploaded_files) == 1
    assert "files/uploaded-big" in deleted_files

    # 4. Invalid schema JSON triggers quarantine return (None, raw_response)
    mode_state["response_text"] = '{"not_a_valid_field": 123}'
    parsed_bad, err_bad = extractor.extract_from_pdf(sample_pdf_path, arxiv_id="2606.10001")
    assert parsed_bad is None
    assert err_bad and "not_a_valid_field" in err_bad


def test_deterministic_entity_resolution_preserves_variants_and_merges_cleanly(
    db_conn: sqlite3.Connection,
) -> None:
    seed_paper(db_conn, "2606.20001")
    cur = db_conn.cursor()

    # Distinct benchmark variants MUST stay separate
    id_base = resolve_and_upsert_entity(cur, entity_type="benchmark", raw_name="SWE-bench")
    id_ver = resolve_and_upsert_entity(cur, entity_type="benchmark", raw_name="SWE-bench Verified")
    assert id_base != id_ver

    # Exact URL match resolves alias to existing entity
    id_with_url = resolve_and_upsert_entity(
        cur,
        entity_type="benchmark",
        raw_name="MMLU-Pro",
        url="https://github.com/TIGER-AI-Lab/MMLU-Pro.git",
    )
    id_alias_by_url = resolve_and_upsert_entity(
        cur,
        entity_type="benchmark",
        raw_name="Massive Multitask Pro",
        url="http://www.github.com/tiger-ai-lab/mmlu-pro/tree/main",
    )
    assert id_with_url == id_alias_by_url

    # Manual CLI merge re-points junction rows cleanly
    id_dup = resolve_and_upsert_entity(
        cur, entity_type="benchmark", raw_name="SWE Bench Legacy Alias"
    )
    cur.execute(
        "INSERT INTO paper_benchmarks (arxiv_id, canonical_id, role) VALUES ('2606.20001', ?, 'introduced')",
        (id_dup,),
    )
    db_conn.commit()

    rep = merge_entity_aliases(db_conn, id_dup, id_base)
    assert rep.aliases_moved >= 1
    assert rep.benchmarks_updated == 1
    assert (
        db_conn.execute(
            "SELECT COUNT(*) FROM entities WHERE canonical_id = ?", (id_dup,)
        ).fetchone()[0]
        == 0
    )
    assert (
        db_conn.execute(
            "SELECT canonical_id FROM paper_benchmarks WHERE arxiv_id = '2606.20001'"
        ).fetchone()[0]
        == id_base
    )


def test_pdf_storage_quota_pending_upload_cleanup_and_withdrawn(
    tmp_settings: Settings,
    sample_pdf_path: Path,
    tmp_path: Path,
) -> None:
    # Local text extraction & bibliography stripping
    extracted = extract_local_text(sample_pdf_path)
    assert extracted.page_count == 1
    assert extracted.chars_per_page > 0
    assert "References" not in strip_bibliography("Intro " * 40 + "\n\nReferences\n[1] Ref")

    # GCS 403 -> pending_upload + local temp file STILL deleted!
    failing_bucket = FakeGCSBucket("inversion", fail_uploads_with=PermissionError("403 Forbidden"))
    gcs = FakeGCSClient({"inversion": failing_bucket})
    gcs.bucket("arxiv-dataset").store["arxiv/arxiv/pdf/2606/2606.30001v1.pdf"] = (
        sample_pdf_path.read_bytes()
    )

    storage = PdfStorageManager(tmp_settings, gcs_client=gcs, export_delay_seconds=0.0)
    staged = storage.stage_pdf("2606.30001", version=1)
    assert staged.local_path.exists()
    res = storage.archive_and_cleanup(staged, published_date="2026-06-01")
    assert res.pdf_sync_status == "pending_upload"
    assert not staged.local_path.exists()

    # Staging budget cap blocks download when exceeded
    tight_settings = Settings(**{**tmp_settings.__dict__, "max_staging_gb": 0.000001})
    tight_settings.staging_dir.mkdir(parents=True, exist_ok=True)
    (tight_settings.staging_dir / "big.pdf").write_bytes(b"x" * 4096)
    tight_mgr = PdfStorageManager(tight_settings, gcs_client=gcs)
    with pytest.raises(StagingQuotaError):
        tight_mgr.enforce_staging_budget()

    # Withdrawn HTML response raises WithdrawnPaperError
    class _WithdrawnSession:
        def get(self, *args: Any, **kwargs: Any) -> Any:
            return SimpleNamespace(
                status_code=200,
                headers={"Content-Type": "text/html; charset=utf-8"},
                content=b"<html>Withdrawn</html>",
                raise_for_status=lambda: None,
            )

    w_mgr = PdfStorageManager(
        tmp_settings,
        gcs_client=FakeGCSClient(),
        http_session=_WithdrawnSession(),  # type: ignore[arg-type]
        export_delay_seconds=0.0,
    )
    with pytest.raises(WithdrawnPaperError):
        w_mgr.stage_pdf("2606.99999")


def test_semantic_scholar_client_preserves_null_on_429_and_links_citations(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    seed_paper(db_conn, "2606.40001", extraction_json='{"contribution_type":"introduces"}')
    seed_paper(db_conn, "2606.40002", extraction_json='{"contribution_type":"introduces"}')

    # Simulate 429 throttle -> citation_count must stay NULL (NEVER 0!)
    class _ThrottleSession:
        def post(self, *args: Any, **kwargs: Any) -> Any:
            return SimpleNamespace(status_code=429, text="Too Many Requests")

    s2_err = SemanticScholarClient(
        tmp_settings,
        session=_ThrottleSession(),  # type: ignore[arg-type]
        max_retries=1,
        delay_seconds=0.0,
    )
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        st_err = s2_err.enrich_papers(db_conn, writer)
    assert st_err.failed_batches == 1
    row = db_conn.execute(
        "SELECT citation_count, s2_last_error FROM papers WHERE arxiv_id = '2606.40001'"
    ).fetchone()
    assert row["citation_count"] is None
    assert "429" in row["s2_last_error"]

    # Now simulate clean 200 response with citations + references matched by requested order
    class _OkSession:
        def post(self, *args: Any, **kwargs: Any) -> Any:
            req_ids = kwargs["json"]["ids"]
            p1_rec = {
                "paperId": "s2_p1",
                "citationCount": 42,
                "influentialCitationCount": 7,
                "venue": "NeurIPS 2026",
                "references": [
                    {
                        "paperId": "s2_ref1",
                        "title": "BBQ: A Hand-Built Bias Benchmark",
                        "externalIds": {"ArXiv": "2110.08193"},
                    }
                ],
            }
            payload = [p1_rec if rid == "ARXIV:2606.40001" else None for rid in req_ids]
            return SimpleNamespace(status_code=200, json=lambda: payload)

    s2_ok = SemanticScholarClient(
        tmp_settings,
        session=_OkSession(),  # type: ignore[arg-type]
        max_retries=1,
        delay_seconds=0.0,
    )
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        st_ok = s2_ok.enrich_papers(db_conn, writer)
    assert st_ok.enriched == 1
    assert st_ok.not_found == 1
    assert st_ok.citations_linked == 1
    row2 = db_conn.execute(
        "SELECT citation_count, venue, s2_last_error FROM papers WHERE arxiv_id = '2606.40001'"
    ).fetchone()
    assert int(row2["citation_count"]) == 42
    assert row2["venue"] == "NeurIPS 2026"
    assert row2["s2_last_error"] is None


def test_controlled_modalities_domains_and_extract_queue_filter(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    fake_gcs: FakeGCSClient,
) -> None:
    # Controlled schema normalizes verbose/underscore inputs cleanly and exposes JSON Schema enums
    parsed = BenchmarkExtraction(
        contribution_type="introduces",
        modalities=[
            "text",
            "image",
            "3d-point-clouds",
            "3d-mesh-geometric-data",
            "audio",
            "speech",
            "electrical-impedance-voltage-and-current-sensor-signals",
            "code_software",
        ],
        domains=[
            "natural-language-processing",
            "biomedical-imaging",
            "medicine",
            "human-robot-interaction-hri",
            "machine-learning-engineering",
            "traffic-monitoring",
        ],
    )
    assert parsed.modalities == [
        "text-llm",
        "vision",
        "3d-spatial",
        "audio-speech",
        "scientific-signals",
        "code-software",
    ]
    assert parsed.domains == [
        "nlp-language",
        "medical-healthcare",
        "robotics-autonomous",
        "software-engineering",
        "industrial-engineering",
    ]
    schema = BenchmarkExtraction.model_json_schema()
    assert "enum" in schema["properties"]["modalities"]["items"]
    assert "enum" in schema["properties"]["domains"]["items"]

    # Stage 2 queue excludes Stage 1 uses_only/unrelated papers even when p >= 0.50
    seed_paper(db_conn, "2611.90001", published_date="2026-11-12")
    seed_paper(db_conn, "2611.90002", published_date="2026-11-12")
    seed_paper(db_conn, "2611.90003", published_date="2026-11-12")
    for aid, contrib in (
        ("2611.90001", "introduces"),
        ("2611.90002", "unrelated"),
        ("2611.90003", "uses_only"),
    ):
        db_conn.execute(
            """
            INSERT INTO triage_assessments (
                arxiv_id, paper_version, rubric_id, rubric_version, question_id,
                model_id, choice_or_bool, probability, assessed_at
            ) VALUES (?, 1, 'ai_benchmark_triage', 'v2.0', 'is_benchmark_contribution',
                      'models/gemini-3.8-flash', 'true', 0.65, '2026-11-14T00:00:00Z')
            """,
            (aid,),
        )
        db_conn.execute(
            """
            INSERT INTO triage_assessments (
                arxiv_id, paper_version, rubric_id, rubric_version, question_id,
                model_id, choice_or_bool, probability, assessed_at
            ) VALUES (?, 1, 'ai_benchmark_triage', 'v2.0', 'contribution_type',
                      'models/gemini-3.8-flash', ?, 0.80, '2026-11-14T00:00:00Z')
            """,
            (aid, contrib),
        )
    db_conn.commit()

    storage = PdfStorageManager(tmp_settings, gcs_client=fake_gcs)
    extractor = ExtractionClient(tmp_settings, storage)
    dry = extractor.estimate_dry_run(db_conn, threshold=0.50)
    assert dry.pending_papers == 1
