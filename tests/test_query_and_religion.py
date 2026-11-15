"""Unit tests for FTS5 query sanitization, coverage matrix, health alerts, and religious-bias parity."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from arxiv_bench.config import Settings
from arxiv_bench.pdf_storage import PdfStorageManager, compress_text
from arxiv_bench.query import (
    build_coverage_matrix,
    format_bibtex,
    get_pipeline_status,
    merge_entity_aliases,
    render_matrix,
    render_search_results,
    sanitize_fts5_query,
    search_papers,
)
from arxiv_bench.religion import (
    generate_daily_update,
    generate_full_reports,
    generate_nonbias_religion_ethics_report,
    generate_wider_net_report,
    select_pending_religion_candidates,
    verify_talk_fact_quote,
)
from tests.conftest import FakeGCSClient, seed_paper


def test_fts5_sanitization_and_search_formats(db_conn: sqlite3.Connection) -> None:
    assert sanitize_fts5_query("SWE-bench AND agent:tool") == '"SWE-bench" AND "agent:tool"'
    assert sanitize_fts5_query("MMLU-Pro v2.0") == '"MMLU-Pro" "v2.0"'

    seed_paper(
        db_conn,
        "2607.00001",
        title="SWE-bench Clinical Agent:Tool Evaluation",
        abstract="Evaluates tool-using coding agents on SWE-bench tasks.",
        extraction_json=json.dumps({"contribution_type": "introduces"}),
    )
    db_conn.execute("INSERT INTO paper_modalities VALUES ('2607.00001', 'code_software')")
    db_conn.commit()

    results = search_papers(db_conn, "SWE-bench", modality="code_software")
    assert len(results) == 1
    assert results[0]["arxiv_id"] == "2607.00001"

    bib = format_bibtex(results[0])
    assert "@misc{" in bib and "2607.00001" in bib
    assert "SWE-bench" in render_search_results(results, fmt="md")
    assert "2607.00001" in render_search_results(results, fmt="csv")


def test_coverage_matrix_across_junctions_and_decision_scores(db_conn: sqlite3.Connection) -> None:
    seed_paper(
        db_conn,
        "2607.00101",
        extraction_json=json.dumps(
            {"contribution_type": "introduces", "evaluation_methods": ["llm-judge"]}
        ),
    )
    seed_paper(
        db_conn,
        "2607.00102",
        extraction_json=json.dumps(
            {"contribution_type": "audits_critiques", "evaluation_methods": ["unit-test"]}
        ),
    )
    db_conn.execute("INSERT INTO paper_modalities VALUES ('2607.00101', 'text_llm')")
    db_conn.execute("INSERT INTO paper_modalities VALUES ('2607.00102', 'code_software')")
    db_conn.execute("INSERT INTO paper_domains VALUES ('2607.00101', 'medical')")
    db_conn.execute("INSERT INTO paper_domains VALUES ('2607.00102', 'software')")
    db_conn.execute(
        """
        INSERT INTO decision_scores (
            arxiv_id, rubric_id, rubric_version, question_id, model_id,
            choice_or_score, probability, entropy, scored_at
        ) VALUES ('2607.00101', 'gap_analysis_core', 'v1.0', 'open_artifact_release',
                  'models/gemini-decision-1', 'true', 0.95, 0.28, '2026-07-01T00:00:00Z')
        """
    )
    db_conn.commit()

    mat = build_coverage_matrix(db_conn, "modality", "domain")
    assert mat.counts[("text_llm", "medical")] == 1
    assert ("text_llm", "software") in mat.zero_cells
    assert "Zero-count gap cells" in render_matrix(mat, fmt="table")

    mat_score = build_coverage_matrix(
        db_conn, "modality", "gap_analysis_core:open_artifact_release"
    )
    assert mat_score.counts[("text_llm", "true")] == 1

    # Newer rubric version supersedes older version without double-counting
    db_conn.execute(
        """
        INSERT INTO decision_scores (
            arxiv_id, rubric_id, rubric_version, question_id, model_id,
            choice_or_score, probability, entropy, scored_at
        ) VALUES ('2607.00101', 'gap_analysis_core', 'v1.1', 'open_artifact_release',
                  'models/gemini-decision-1', 'false', 0.12, 0.35, '2026-07-02T00:00:00Z')
        """
    )
    db_conn.commit()
    mat_latest = build_coverage_matrix(
        db_conn, "modality", "gap_analysis_core:open_artifact_release"
    )
    assert mat_latest.counts.get(("text_llm", "false")) == 1
    assert mat_latest.counts.get(("text_llm", "true"), 0) == 0
    mat_pinned = build_coverage_matrix(
        db_conn, "modality", "gap_analysis_core@v1.0:open_artifact_release"
    )
    assert mat_pinned.counts.get(("text_llm", "true")) == 1


def test_status_alerts_on_stale_watermark(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    stale_ts = (datetime.now(UTC) - timedelta(hours=72)).isoformat()
    db_conn.execute(
        """
        INSERT INTO ingestion_checkpoints (source, watermark_date, cursor_state, malformed_lines, updated_at)
        VALUES ('arxiv_atom_delta', '2026-10-23', 'ok', 0, ?)
        """,
        (stale_ts,),
    )
    db_conn.commit()
    status = get_pipeline_status(db_conn, tmp_settings)
    assert any("stale" in a.lower() for a in status.alerts)


def test_religion_orthogonal_routing_daily_scoping_and_talk_facts_cleanup(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    fake_gcs: FakeGCSClient,
    sample_pdf_path: Path,
    tmp_path: Path,
) -> None:
    # Empirical uses_only paper on BBQ: excluded from v_benchmarks, MUST still route to religion!
    seed_paper(
        db_conn,
        "2610.29657",
        title="Testing LLMs on BBQ Religious Stereotypes",
        categories=["cs.CL", "stat.ML"],
        extraction_json=json.dumps({"contribution_type": "uses_only"}),
        gcs_pdf_uri="gs://inversion/pdf/2610/2610.29657.pdf",
    )
    db_conn.execute(
        """
        INSERT INTO triage_assessments (
            arxiv_id, paper_version, rubric_id, rubric_version, question_id,
            model_id, choice_or_bool, probability, assessed_at
        ) VALUES ('2610.29657', 1, 'ai_benchmark_triage', 'v2.0',
                  'is_llm_bias_ethics_religion', 'models/gemini-decision-1', 'true', 0.91, '2026-10-22T00:00:00Z')
        """
    )
    db_conn.commit()

    # Excluded from general benchmark view, included in religion queue
    assert db_conn.execute("SELECT COUNT(*) FROM v_benchmarks").fetchone()[0] == 0
    pending = select_pending_religion_candidates(db_conn, threshold=0.40)
    assert [r["arxiv_id"] for r in pending] == ["2610.29657"]

    # Register one daily run and one backfill run; daily-update must ONLY include mode='daily'
    db_conn.execute(
        "INSERT INTO pipeline_runs (run_id, mode, started_at, status) VALUES ('run_daily_1', 'daily', '2026-10-22T00:00:00Z', 'completed')"
    )
    db_conn.execute(
        "INSERT INTO pipeline_runs (run_id, mode, started_at, status) VALUES ('run_backfill_1', 'backfill', '2026-10-22T00:00:00Z', 'completed')"
    )
    seed_paper(db_conn, "2601.11111", title="Old Backfill Paper")
    db_conn.execute(
        """
        INSERT INTO religious_bias_details (
            arxiv_id, religion_component, measurement_description, religious_groups_json,
            models_tested_json, languages_json, response_type_json, base_benchmarks_json,
            continuous_testing, findings, extracted_at, run_id
        ) VALUES ('2610.29657', 'major', 'Evaluates BBQ.', '["Mormon","Islam"]',
                  '["GPT-4o"]', '["English"]', '["multiple-choice"]', '["BBQ"]',
                  0, 'Found bias against Latter-day Saints.', '2026-10-22T01:00:00Z', 'run_daily_1')
        """
    )
    db_conn.execute(
        """
        INSERT INTO religious_bias_details (
            arxiv_id, religion_component, measurement_description, findings, extracted_at, run_id
        ) VALUES ('2601.11111', 'major', 'Historical', 'Historical finding', '2026-10-22T01:00:00Z', 'run_backfill_1')
        """
    )
    db_conn.execute(
        "INSERT INTO paper_bias_targets VALUES ('2610.29657', 'Religious bias', 'QA', 1)"
    )
    db_conn.execute(
        """
        UPDATE papers
        SET legacy_metadata_json = '{"is_llm_related": true, "is_bias_related": false, "ethics": true, "reasoning": "Ethics only"}'
        WHERE arxiv_id = '2601.11111'
        """
    )
    db_conn.commit()

    daily_out = tmp_path / "daily.md"
    assert generate_daily_update(db_conn, "run_daily_1", daily_out) == 1
    txt = daily_out.read_text(encoding="utf-8")
    assert "#Mormon" in txt and "#ReligionFocus" in txt
    assert "2610.29657" in txt
    assert "2601.11111" not in txt

    # Backfill run produces 0 daily update rows
    assert generate_daily_update(db_conn, "run_backfill_1", tmp_path / "backfill.md") == 0

    # Full reports, non-bias report, and wider-net report
    counts = generate_full_reports(db_conn, tmp_path / "reports")
    assert counts.religion_papers == 2
    assert counts.religion_primary_papers == 1
    assert generate_nonbias_religion_ethics_report(db_conn, tmp_path / "nonbias.md") == 1
    assert generate_wider_net_report(db_conn, tmp_path / "wider.md") == 1

    # Talk facts quote verification: checks stored text first, then streams GCS PDF and cleans up
    db_conn.execute(
        "UPDATE papers SET compressed_text_zst = ? WHERE arxiv_id = '2610.29657'",
        (compress_text("In our experiments on BBQ, religious bias reached 42%."),),
    )
    db_conn.commit()
    storage = PdfStorageManager(tmp_settings, gcs_client=fake_gcs)
    v1 = verify_talk_fact_quote(db_conn, storage, arxiv_id="2610.29657", claim_keywords=["42%"])
    assert v1["verified"] is True and v1["source"] == "stored_text"

    # Force visual PDF streaming from GCS and verify temp file is removed after check
    fake_gcs.bucket("inversion").store["pdf/2610/2610.29657.pdf"] = sample_pdf_path.read_bytes()
    v2 = verify_talk_fact_quote(
        db_conn,
        storage,
        arxiv_id="2610.29657",
        claim_keywords=["Benchmark"],
        require_visual_pdf=True,
    )
    assert v2["verified"] is True and v2["source"] == "gcs_pdf_streamed"
    assert list(tmp_settings.staging_dir.glob("*.pdf")) == []


def test_query_filters_matrix_dimensions_alias_merge_and_renderers(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    assert sanitize_fts5_query("   ") == ""
    assert sanitize_fts5_query('"exact phrase" benchmark') == '"exact phrase" benchmark'
    assert search_papers(db_conn, "   ") == []

    seed_paper(
        db_conn,
        "2608.00001",
        title="MedAgentBench Clinical Benchmark",
        abstract="Evaluates clinical reasoning agents.",
        published_date="2026-08-05",
        extraction_json=json.dumps(
            {"contribution_type": "introduces", "evaluation_methods": ["llm-judge"]}
        ),
    )
    db_conn.execute(
        "UPDATE papers SET venue = 'NeurIPS 2026', citation_count = 12 WHERE arxiv_id = '2608.00001'"
    )
    db_conn.execute("INSERT INTO paper_modalities VALUES ('2608.00001', 'agentic_tool_use')")
    db_conn.execute("INSERT INTO paper_domains VALUES ('2608.00001', 'medical')")
    db_conn.execute("INSERT INTO paper_tasks VALUES ('2608.00001', 'clinical-qa')")
    db_conn.execute(
        """
        INSERT INTO decision_scores (
            arxiv_id, rubric_id, rubric_version, question_id, model_id,
            choice_or_score, probability, entropy, scored_at
        ) VALUES ('2608.00001', 'gap_analysis_core', 'v1.0', 'open_artifact_release',
                  'models/gemini-decision-1', 'true', 0.92, 0.4, '2026-08-06T00:00:00Z')
        """
    )
    db_conn.execute(
        """
        INSERT INTO religious_bias_details (
            arxiv_id, religion_component, measurement_description, findings, extracted_at
        ) VALUES ('2608.00001', 'minor', 'desc', 'finding', '2026-08-06T00:00:00Z')
        """
    )
    db_conn.commit()

    hits = search_papers(
        db_conn,
        "MedAgentBench",
        modality="agentic_tool_use",
        domain="medical",
        contribution_type="introduces",
        rubric_filter=("gap_analysis_core", "open_artifact_release", "true"),
        religion_only=True,
    )
    assert len(hits) == 1
    assert "@inproceedings{" in format_bibtex(hits[0])
    assert "2608.00001" in render_search_results(hits, fmt="json")
    assert "@inproceedings{" in render_search_results(hits, fmt="bibtex")
    assert "2608.00001" in render_search_results(hits, fmt="table")

    # Exercise every matrix dimension + filter + renderer
    for rows_d, cols_d in [
        ("task", "contribution_type"),
        ("year", "evaluation_method"),
    ]:
        m = build_coverage_matrix(
            db_conn,
            rows_d,
            cols_d,
            domain="medical",
            modality="agentic_tool_use",
            year_from=2025,
        )
        assert m.counts
        assert m.rows_dim in render_matrix(m, fmt="json")
        assert render_matrix(m, fmt="csv")
        assert "|" in render_matrix(m, fmt="md")

    with pytest.raises(ValueError):
        build_coverage_matrix(db_conn, "unknown_dim", "domain")

    # Entity alias merge + error checks
    db_conn.execute(
        "INSERT INTO entities (canonical_id, entity_type, canonical_name, canonical_url) "
        "VALUES ('b_src', 'benchmark', 'MedBench Old', 'https://github.com/org/med')"
    )
    db_conn.execute(
        "INSERT INTO entities (canonical_id, entity_type, canonical_name) "
        "VALUES ('b_dst', 'benchmark', 'MedBench')"
    )
    db_conn.execute(
        "INSERT INTO entities (canonical_id, entity_type, canonical_name) "
        "VALUES ('m_other', 'model', 'GPT-5')"
    )
    db_conn.execute(
        "INSERT INTO entity_aliases (raw_slug, entity_type, canonical_id, resolution_method) "
        "VALUES ('medbench-old', 'benchmark', 'b_src', 'slug')"
    )
    db_conn.execute("INSERT INTO paper_benchmarks VALUES ('2608.00001', 'b_src', 'introduces')")
    db_conn.commit()

    with pytest.raises(ValueError):
        merge_entity_aliases(db_conn, "b_src", "b_src")
    with pytest.raises(ValueError):
        merge_entity_aliases(db_conn, "missing", "b_dst")
    with pytest.raises(ValueError):
        merge_entity_aliases(db_conn, "b_src", "missing")
    with pytest.raises(ValueError):
        merge_entity_aliases(db_conn, "b_src", "m_other")

    merged = merge_entity_aliases(db_conn, "b_src", "b_dst")
    assert merged.aliases_moved == 1
    assert merged.benchmarks_updated == 1
    dst = db_conn.execute(
        "SELECT canonical_url FROM entities WHERE canonical_id = 'b_dst'"
    ).fetchone()
    assert dst["canonical_url"] == "https://github.com/org/med"

    # Status alerts: missing checkpoint, incomplete pagination, pending uploads, old backup
    st_empty = get_pipeline_status(db_conn, tmp_settings)
    assert any("No ingestion checkpoints" in a for a in st_empty.alerts)

    db_conn.execute(
        "UPDATE papers SET pdf_sync_status = 'pending_upload' WHERE arxiv_id = '2608.00001'"
    )
    db_conn.execute(
        "INSERT INTO ingestion_checkpoints (source, watermark_date, cursor_state, malformed_lines, updated_at) "
        "VALUES ('arxiv_atom_delta', '2026-08-06', 'incomplete_pagination', 1, 'not-a-timestamp')"
    )
    db_conn.commit()
    backup_file = tmp_settings.db_path.parent / "backups" / "latest.db.zst"
    backup_file.parent.mkdir(parents=True, exist_ok=True)
    backup_file.write_bytes(b"fake")
    st_alerts = get_pipeline_status(
        db_conn,
        tmp_settings,
        now_utc=datetime.now(UTC) + timedelta(hours=100),
    )
    assert any("incomplete_pagination" in a for a in st_alerts.alerts)
    assert any("pending_upload" in a for a in st_alerts.alerts)
    assert any("backup is older" in a for a in st_alerts.alerts)
