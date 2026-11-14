"""Regression tests for migrate_legacy.py reproducing every real /mnt/filestore corruption mode."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from arxiv_bench.config import Settings
from arxiv_bench.db import connect_db
from arxiv_bench.migrate_legacy import migrate_legacy
from tests.conftest import FakeGCSClient


def _build_corrupted_legacy_tree(root: Path) -> None:
    (root / "utility_files").mkdir(parents=True)
    (root / "json" / "2_paper_metadata").mkdir(parents=True)
    (root / "json" / "3_paper_bias_targets").mkdir(parents=True)
    (root / "json" / "4_religious_bias_analysis").mkdir(parents=True)

    # 1. Mixed 12-column and 16-column rows under a 12-column header (exact live repo bug!)
    with (root / "utility_files" / "1st_pass_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            [
                "filename",
                "date",
                "title",
                "page_count",
                "is_benchmark",
                "is_llm_related",
                "is_bias_related",
                "is_faith_ethics_related",
                "is_survey_review",
                "reference_count",
                "appendix_length",
                "reasoning",
            ]
        )
        # 12-column row
        w.writerow(
            [
                "2501.00001.pdf",
                "2025-01-10",
                "Legacy 12-Col Paper",
                "14",
                "True",
                "True",
                "True",
                "False",
                "False",
                "55",
                "2",
                "12-col reasoning",
            ]
        )
        # 16-column shifted row (inserts bias_and_fairness, moral_reasoning, ethics, religion before reference_count!)
        w.writerow(
            [
                "2603.11936.pdf",
                "2026-03-12",
                "Shifted 16-Col Paper",
                "9",
                "False",
                "True",
                "True",
                "False",
                "False",
                "True",
                "False",
                "True",
                "True",
                "31",
                "1",
                "16-col reasoning",
            ]
        )

    # 2. Stage 2 JSONs: one valid + one raw_response poison
    (root / "json" / "2_paper_metadata" / "2501.00001.json").write_text(
        json.dumps(
            {
                "date": "2025-01-10",
                "title": "Legacy 12-Col Paper",
                "is_benchmark": True,
                "is_llm_related": True,
                "is_bias_related": True,
            }
        ),
        encoding="utf-8",
    )
    (root / "json" / "2_paper_metadata" / "2501.99999.json").write_text(
        json.dumps({"raw_response": "Broken unclosed JSON..."}),
        encoding="utf-8",
    )

    # 3. Stage 3 polymorphic bias_targets (old list[str] + new list[dict])
    (root / "json" / "3_paper_bias_targets" / "2501.00001.json").write_text(
        json.dumps(
            {
                "title": "Legacy 12-Col Paper",
                "bias_targets": ["gender", "religion bias"],
                "primary_bias_target": "religion bias",
            }
        ),
        encoding="utf-8",
    )
    (root / "json" / "3_paper_bias_targets" / "2603.11936.json").write_text(
        json.dumps(
            {
                "title": "Shifted 16-Col Paper",
                "bias_targets": [{"target": "religious bias", "methodology": "BBQ prompts"}],
                "primary_bias_target": "religious bias",
            }
        ),
        encoding="utf-8",
    )

    # 4. Stage 4 renamed field benchmark_measurement vs measurement_description
    (root / "json" / "4_religious_bias_analysis" / "2501.00001.json").write_text(
        json.dumps(
            {
                "title": "Legacy 12-Col Paper",
                "religion_component": "major",
                "benchmark_measurement": "Old field name measurement",
                "religious_groups": ["Christian", "Muslim"],
                "models_tested": ["GPT-4"],
                "languages_evaluated": ["English"],
                "response_type": ["open-ended"],
                "base_benchmarks": ["BBQ"],
                "continuous_testing": False,
                "findings": "Significant religious stereotype disparity.",
            }
        ),
        encoding="utf-8",
    )

    # 5. download_assessments_cache.json (unversioned booleans)
    (root / "utility_files" / "download_assessments_cache.json").write_text(
        json.dumps(
            {
                "2501.00001": True,
                "2603.11936": False,
                "2201.00000": False,  # untracked old negative -> stays open for ai_benchmark_triage v2.0
            }
        ),
        encoding="utf-8",
    )

    # 6. citations_cache.json
    (root / "utility_files" / "citations_cache.json").write_text(
        json.dumps({"2501.00001": {"count": 19, "timestamp": "2026-06-29T03:48:38"}}),
        encoding="utf-8",
    )

    # 7. Code-bug failures that must be requeued, not permanently blacklisted
    with (root / "utility_files" / "2nd_pass_failures.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(["filename", "error", "timestamp"])
        w.writerow(["2508.05929.pdf", "'list' object is not a mapping", "2026-03-15 10:30:09"])
    with (root / "utility_files" / "3rd_pass_failures.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(["filename", "error", "timestamp"])
        w.writerow(
            [
                "2503.19540.pdf",
                "the JSON object must be str, bytes or bytearray, not NoneType",
                "2026-01-25 13:48:07",
            ]
        )

    # 8. Minimal local legacy arXiv snapshot line for categories/abstract enrichment
    (root / "utility_files" / "arxiv-metadata-oai-snapshot.json").write_text(
        json.dumps(
            {
                "id": "2501.00001",
                "title": "Legacy 12-Col Paper",
                "abstract": "Evaluates religious bias across LLMs.",
                "categories": "cs.CL stat.ML",
                "authors_parsed": [["Doe", "Jane", ""]],
                "versions": [{"version": "v1"}, {"version": "v2"}],
                "update_date": "2025-01-15",
            }
        )
        + "\n",
        encoding="utf-8",
    )


def test_migrate_legacy_repairs_all_corruptions_and_is_idempotent(
    tmp_settings: Settings,
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "legacy_nfs"
    _build_corrupted_legacy_tree(legacy_root)

    gcs = FakeGCSClient()
    gcs.bucket("inversion").store["pdf/2501.00001.pdf"] = b"%PDF-1.4 fake"
    gcs.bucket("inversion").store["pdf/cs/0311046.pdf"] = b"%PDF-1.4 fake"

    rep1 = migrate_legacy(legacy_root, tmp_settings, index_gcs=True, gcs_client=gcs, io_workers=2)
    assert rep1.csv_rows_12 == 1
    assert rep1.csv_rows_16 == 1
    assert rep1.csv_rows_malformed == 0
    assert rep1.stage2_quarantined == 1
    assert rep1.stage3_papers_imported == 2
    assert rep1.stage4_imported == 1
    assert rep1.legacy_cache_positives == 1
    assert rep1.legacy_cache_negatives_untracked == 1
    assert rep1.citations_imported == 1
    assert rep1.bug_failures_requeued == 2
    assert rep1.gcs_pdfs_indexed == 1
    assert rep1.snapshot_enriched == 1

    conn = connect_db(tmp_settings.db_path, readonly=True)
    try:
        # Verify 16-column row repaired accurately (reference_count=31, religion=True, NOT shifted!)
        r16 = conn.execute(
            "SELECT page_count, legacy_metadata_json FROM papers WHERE arxiv_id = '2603.11936'"
        ).fetchone()
        assert int(r16["page_count"]) == 9
        meta16 = json.loads(r16["legacy_metadata_json"])
        assert meta16["religion"] is True
        assert meta16["reference_count"] == 31
        assert meta16["reasoning"] == "16-col reasoning"

        # Verify Stage 4 benchmark_measurement mapped to measurement_description
        r4 = conn.execute(
            "SELECT measurement_description FROM religious_bias_details WHERE arxiv_id = '2501.00001'"
        ).fetchone()
        assert r4["measurement_description"] == "Old field name measurement"

        # Verify raw_response JSON quarantined
        q = conn.execute(
            "SELECT status FROM paper_stage_status WHERE arxiv_id = '2501.99999' AND stage = 'legacy_stage2'"
        ).fetchone()
        assert q["status"] == "quarantined_invalid_schema"

        # Verify bug failures requeued to pending under their respective stages
        rq2 = conn.execute(
            "SELECT status, last_error_code FROM paper_stage_status "
            "WHERE arxiv_id = '2508.05929' AND stage = 'religion_bias_targets'"
        ).fetchone()
        assert rq2["status"] == "pending" and rq2["last_error_code"] == "REQUEUED_LEGACY_BUG"
        rq3 = conn.execute(
            "SELECT status, last_error_code FROM paper_stage_status "
            "WHERE arxiv_id = '2503.19540' AND stage = 'religion_extract'"
        ).fetchone()
        assert rq3["status"] == "pending" and rq3["last_error_code"] == "REQUEUED_LEGACY_BUG"

        # Verify legacy cache stamped with legacy_llm_bias_v1
        ta = conn.execute(
            "SELECT rubric_version, choice_or_bool FROM triage_assessments WHERE arxiv_id = '2501.00001'"
        ).fetchone()
        assert ta["rubric_version"] == "legacy_llm_bias_v1" and ta["choice_or_bool"] == "true"

        # Verify GCS URI indexed without rewriting object
        uri_row = conn.execute(
            "SELECT gcs_pdf_uri, pdf_sync_status, citation_count FROM papers WHERE arxiv_id = '2501.00001'"
        ).fetchone()
        assert uri_row["gcs_pdf_uri"] == "gs://inversion/pdf/2501.00001.pdf"
        assert uri_row["pdf_sync_status"] == "synced"
        assert int(uri_row["citation_count"]) == 19

        baseline_papers = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
        baseline_targets = conn.execute("SELECT COUNT(*) FROM paper_bias_targets").fetchone()[0]
    finally:
        conn.close()

    # Second run must be completely idempotent
    migrate_legacy(legacy_root, tmp_settings, index_gcs=True, gcs_client=gcs, io_workers=2)
    conn2 = connect_db(tmp_settings.db_path, readonly=True)
    try:
        assert conn2.execute("SELECT COUNT(*) FROM papers").fetchone()[0] == baseline_papers
        assert (
            conn2.execute("SELECT COUNT(*) FROM paper_bias_targets").fetchone()[0]
            == baseline_targets
        )
    finally:
        conn2.close()


def test_migrate_legacy_dry_run_malformed_and_stage3_stage4_quarantine(
    tmp_settings: Settings,
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "legacy_edge"
    (legacy_root / "utility_files").mkdir(parents=True)
    (legacy_root / "json" / "3_paper_bias_targets").mkdir(parents=True)
    (legacy_root / "json" / "4_religious_bias_analysis").mkdir(parents=True)

    # CSV with empty row, malformed width row, and non-numeric int
    with (legacy_root / "utility_files" / "1st_pass_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(
            [
                "filename",
                "date",
                "title",
                "page_count",
                "is_benchmark",
                "is_llm_related",
                "is_bias_related",
                "is_faith_ethics_related",
                "is_survey_review",
                "reference_count",
                "appendix_length",
                "reasoning",
            ]
        )
        w.writerow([])
        w.writerow(["bad_row_width", "only_3_cols", "oops"])
        w.writerow(
            [
                "2502.00001.pdf",
                "2025-02-01",
                "Bad Ints",
                "not_an_int",
                "maybe",
                "True",
                "False",
                "False",
                "False",
                "",
                "3",
                "ok",
            ]
        )

    # Dry run parses CSV only without creating DB
    dry = migrate_legacy(legacy_root, tmp_settings, dry_run=True)
    assert dry.csv_rows_12 == 1
    assert dry.csv_rows_malformed == 1
    assert not tmp_settings.db_path.exists()

    # Poison Stage 3 & Stage 4 JSONs + broken syntax JSON + non-object JSON + string-typed Stage 4 fields
    (legacy_root / "json" / "3_paper_bias_targets" / "2502.99991.json").write_text(
        json.dumps({"raw_response": "broken stage3"}), encoding="utf-8"
    )
    (legacy_root / "json" / "3_paper_bias_targets" / "2502.99992.json").write_text(
        "[1, 2, 3]", encoding="utf-8"
    )
    (legacy_root / "json" / "4_religious_bias_analysis" / "2502.99993.json").write_text(
        "{not valid json", encoding="utf-8"
    )
    (legacy_root / "json" / "4_religious_bias_analysis" / "2502.00001.json").write_text(
        json.dumps(
            {
                "title": "String List Fields Paper",
                "religion_component": "minor",
                "measurement_description": "Measures prompt bias",
                "religious_groups": "Islam",
                "models_tested": "GPT-4",
                "languages_evaluated": "English",
                "response_type": "open-ended",
                "base_benchmarks": "",
                "continuous_testing": "true",
                "findings": "Minor shift.",
            }
        ),
        encoding="utf-8",
    )
    # Cache with untracked positive and citations_cache with malformed entries
    (legacy_root / "utility_files" / "download_assessments_cache.json").write_text(
        json.dumps({"2502.77777": True}), encoding="utf-8"
    )
    (legacy_root / "utility_files" / "citations_cache.json").write_text(
        json.dumps({"2502.00001": "bad", "2502.77777": {"count": None}}), encoding="utf-8"
    )

    rep = migrate_legacy(legacy_root, tmp_settings, io_workers=2)
    assert rep.stage3_quarantined == 2
    assert rep.stage4_quarantined == 1
    assert rep.stage4_imported == 1
    assert rep.legacy_cache_positives == 1
    assert rep.citations_imported == 0
