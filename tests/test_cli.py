"""CLI smoke and integration tests for offline subcommands."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from arxiv_bench.cli import main
from arxiv_bench.config import Settings, canonicalize_arxiv_id, format_yymm_prefix
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.decision_client import (
    DailyQuotaExceededError,
    DecisionAnswerRecord,
    DecisionCallOutput,
    PermanentDecisionError,
    is_daily_quota_error,
)
from arxiv_bench.flash_triage import (
    FlashBatchResult,
    FlashBatchTriageResponse,
    FlashPaperTriageItem,
    FlashTriageClient,
    TriagePaperInput,
)
from arxiv_bench.schemas import load_rubric_yaml
from tests.conftest import seed_paper


def test_canonicalize_urls_and_yymm_helpers() -> None:
    assert canonicalize_arxiv_id("http://arxiv.org/abs/cs/0311046v2") == ("cs/0311046", 2)
    assert canonicalize_arxiv_id("https://export.arxiv.org/pdf/2601.15755v1.pdf") == (
        "2601.15755",
        1,
    )
    assert canonicalize_arxiv_id("cs_0311046.json") == ("cs/0311046", None)
    assert format_yymm_prefix("cs/0311046") == "0311"
    assert format_yymm_prefix("custom", published_date="2026-07-04") == "2607"
    assert format_yymm_prefix("custom") == "0000"


def test_cli_offline_subcommands(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    tmp_path: Path,
    capsys: object,
) -> None:
    seed_paper(
        db_conn,
        "2609.00001",
        title="CodeAgentBench Software Benchmark",
        abstract="Introduces a software agent benchmark.",
        extraction_json=json.dumps({"contribution_type": "introduces"}),
    )
    db_conn.execute("INSERT INTO paper_modalities VALUES ('2609.00001', 'code_software')")
    db_conn.execute("INSERT INTO paper_domains VALUES ('2609.00001', 'software')")
    db_conn.execute(
        "INSERT INTO entities (canonical_id, entity_type, canonical_name) "
        "VALUES ('ent_a', 'benchmark', 'CodeAgentBench')"
    )
    db_conn.commit()
    db_conn.close()

    db_arg = str(tmp_settings.db_path)

    assert main(["--db-path", db_arg, "status"]) == 0
    assert main(["--db-path", db_arg, "search", "CodeAgentBench", "--format", "json"]) == 0
    assert (
        main(
            [
                "--db-path",
                db_arg,
                "matrix",
                "--rows",
                "modality",
                "--cols",
                "domain",
                "--format",
                "md",
            ]
        )
        == 0
    )
    assert main(["--db-path", db_arg, "alias", "list"]) == 0
    assert (
        main(
            [
                "--db-path",
                db_arg,
                "backup",
                "--no-gcs",
                "--no-nfs",
                "--verify-restore",
            ]
        )
        == 0
    )
    empty_legacy = tmp_path / "empty_legacy"
    empty_legacy.mkdir()
    assert (
        main(
            [
                "--db-path",
                db_arg,
                "migrate-legacy",
                "--legacy-root",
                str(empty_legacy),
                "--dry-run",
            ]
        )
        == 0
    )


def test_cli_triage_chunked_streaming_and_permanent_failure_skip(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for idx in range(5):
        seed_paper(
            db_conn,
            f"2611.0000{idx}",
            title=f"Paper {idx}",
            abstract=f"Abstract {idx}",
            published_date=f"2026-11-0{idx + 1}",
        )
    db_conn.commit()
    db_conn.close()

    calls: list[str] = []

    class _FakeDecisionClient:
        def __init__(self, settings: Settings) -> None:
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        def score_abstract(
            self,
            *,
            arxiv_id: str,
            paper_version: int,
            title: str,
            abstract: str,
            categories: list[str],
            rubric_pack: Any,
            writer: Any,
            run_id: str,
        ) -> DecisionCallOutput:
            calls.append(arxiv_id)
            if arxiv_id == "2611.00001":
                raise PermanentDecisionError("content blocked", status_code=422)
            if arxiv_id == "2611.00002" and calls.count("2611.00002") == 1:
                raise RuntimeError("transient 503")
            writer.submit_sql(
                """
                INSERT INTO triage_assessments (
                    arxiv_id, paper_version, rubric_id, rubric_version,
                    question_id, model_id, choice_or_bool, probability,
                    distribution_json, assessed_at
                ) VALUES (?, ?, ?, ?, 'is_benchmark_contribution', 'models/gemini-decision-1', 'true', 0.9, '{}', '2026-11-13T00:00:00Z')
                """,
                (arxiv_id, paper_version, rubric_pack.rubric_id, rubric_pack.rubric_version),
            )
            return DecisionCallOutput(
                answers=[
                    DecisionAnswerRecord("is_benchmark_contribution", "true", 0.9, 0.4, {}),
                ],
                input_tokens=1000,
                output_tokens=0,
                estimated_cost_usd=0.0001,
                latency_ms=150,
                http_status=200,
            )

    monkeypatch.setattr("arxiv_bench.cli.DecisionClient", _FakeDecisionClient)
    db_arg = str(tmp_settings.db_path)

    # First run with chunk-size=2 on --backend decisions should process all 5 across 3 chunks
    rc1 = main(
        [
            "--db-path",
            db_arg,
            "triage",
            "--backend",
            "decisions",
            "--chunk-size",
            "2",
            "--workers",
            "2",
        ]
    )
    assert rc1 == 0
    out1 = json.loads(capsys.readouterr().out)
    assert out1["attempted"] == 5
    assert out1["succeeded"] == 3
    assert out1["failed_permanent"] == 1
    assert out1["failed_transient"] == 1

    # Second run must skip the failed_permanent paper (2611.00001) and retry ONLY the transient one (2611.00002)
    rc2 = main(
        [
            "--db-path",
            db_arg,
            "triage",
            "--backend",
            "decisions",
            "--chunk-size",
            "2",
            "--workers",
            "2",
        ]
    )
    assert rc2 == 0
    out2 = json.loads(capsys.readouterr().out)
    assert out2["attempted"] == 1
    assert out2["succeeded"] == 1
    assert out2["failed"] == 0
    assert calls.count("2611.00001") == 1
    assert calls.count("2611.00002") == 2

    # Dry run now reports 0 pending papers
    rc3 = main(["--db-path", db_arg, "triage", "--dry-run"])
    assert rc3 == 0
    out3 = json.loads(capsys.readouterr().out)
    assert out3["pending_papers"] == 0

    # pipeline_runs recorded both runs cleanly
    check_conn = sqlite3.connect(str(tmp_settings.db_path))
    runs = check_conn.execute(
        "SELECT mode, status FROM pipeline_runs ORDER BY started_at"
    ).fetchall()
    check_conn.close()
    assert runs == [("triage", "completed"), ("triage", "completed")]


def test_cli_triage_fast_stops_on_daily_quota(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for idx in range(4):
        seed_paper(
            db_conn,
            f"2611.1000{idx}",
            title=f"Quota Paper {idx}",
            abstract=f"Abstract {idx}",
            published_date=f"2026-11-0{idx + 1}",
        )
    db_conn.commit()
    db_conn.close()

    class _QuotaDecisionClient:
        def __init__(self, settings: Settings, **kwargs: Any) -> None:
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        def score_abstract(self, **kwargs: Any) -> DecisionCallOutput:
            raise DailyQuotaExceededError(
                "429 Too Many Requests: Rate limit exceeded (limit: 50000 requests per day on Tier 1)"
            )

    monkeypatch.setattr("arxiv_bench.cli.DecisionClient", _QuotaDecisionClient)
    rc = main(
        [
            "--db-path",
            str(tmp_settings.db_path),
            "triage",
            "--backend",
            "decisions",
            "--no-fallback-to-flash",
            "--chunk-size",
            "2",
            "--workers",
            "1",
        ]
    )
    assert rc == 2
    out = json.loads(capsys.readouterr().out)
    assert out["stopped_reason"] == "daily_quota_exceeded"
    assert out["fallback_activated"] is False
    assert out["failed_permanent"] == 0
    assert out["attempted"] <= 2


def test_cli_triage_falls_back_to_flash_on_daily_quota(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for idx in range(5):
        seed_paper(
            db_conn,
            f"2611.2000{idx}",
            title=f"Fallback Paper {idx}",
            abstract=f"Abstract {idx}",
            published_date=f"2026-11-0{idx + 1}",
        )
    db_conn.commit()
    db_conn.close()

    dec_calls: list[str] = []
    flash_batches: list[list[str]] = []

    class _PartialQuotaDecisionClient:
        def __init__(self, settings: Settings, **kwargs: Any) -> None:
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        def score_abstract(
            self,
            *,
            arxiv_id: str,
            paper_version: int,
            rubric_pack: Any,
            writer: Any,
            **kwargs: Any,
        ) -> DecisionCallOutput:
            dec_calls.append(arxiv_id)
            if len(dec_calls) == 1:
                writer.submit_sql(
                    """
                    INSERT INTO triage_assessments (
                        arxiv_id, paper_version, rubric_id, rubric_version,
                        question_id, model_id, choice_or_bool, probability,
                        distribution_json, assessed_at
                    ) VALUES (?, ?, ?, ?, 'is_benchmark_contribution', 'models/gemini-decision-1', 'true', 0.91, '{}', '2026-11-14T00:00:00Z')
                    """,
                    (arxiv_id, paper_version, rubric_pack.rubric_id, rubric_pack.rubric_version),
                )
                return DecisionCallOutput(
                    answers=[
                        DecisionAnswerRecord("is_benchmark_contribution", "true", 0.91, 0.2, {}),
                    ],
                    input_tokens=1100,
                    output_tokens=0,
                    estimated_cost_usd=0.00011,
                    latency_ms=120,
                    http_status=200,
                )
            raise DailyQuotaExceededError(
                "429 Too Many Requests: Rate limit exceeded (limit: 50000 requests per day on Tier 1)"
            )

    class _FakeFlashClient:
        def __init__(self, settings: Settings, **kwargs: Any) -> None:
            self._model = kwargs.get("model") or settings.flash_model
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        @property
        def model_name(self) -> str:
            return (
                self._model if str(self._model).startswith("models/") else f"models/{self._model}"
            )

        def score_abstract_batch(
            self,
            *,
            papers: list[TriagePaperInput],
            rubric_pack: Any,
            writer: Any,
            run_id: str,
        ) -> FlashBatchResult:
            flash_batches.append([p.arxiv_id for p in papers])
            for p in papers:
                writer.submit_sql(
                    """
                    INSERT INTO triage_assessments (
                        arxiv_id, paper_version, rubric_id, rubric_version,
                        question_id, model_id, choice_or_bool, probability,
                        distribution_json, assessed_at
                    ) VALUES (?, ?, ?, ?, 'is_benchmark_contribution', ?, 'true', 0.85, '{}', '2026-11-14T00:01:00Z')
                    """,
                    (
                        p.arxiv_id,
                        p.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                        self.model_name,
                    ),
                )
            return FlashBatchResult(
                succeeded_ids=[p.arxiv_id for p in papers],
                input_tokens=330 * len(papers),
                output_tokens=85 * len(papers),
                estimated_cost_usd=0.00031 * len(papers),
                latency_ms=500,
            )

    monkeypatch.setattr("arxiv_bench.cli.DecisionClient", _PartialQuotaDecisionClient)
    monkeypatch.setattr("arxiv_bench.cli.FlashTriageClient", _FakeFlashClient)

    db_arg = str(tmp_settings.db_path)
    rc = main(
        [
            "--db-path",
            db_arg,
            "triage",
            "--backend",
            "decisions",
            "--chunk-size",
            "2",
            "--workers",
            "1",
            "--flash-batch-size",
            "2",
            "--flash-workers",
            "1",
        ]
    )
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["fallback_activated"] is True
    assert "50000 requests per day" in (out["fallback_reason"] or "")
    assert out["flash_model"] == "models/gemini-3.8-flash"
    assert out["succeeded_decisions"] == 1
    assert out["succeeded_flash"] == 4
    assert out["succeeded"] == 5
    assert out["attempted"] == 5
    assert out["failed"] == 0
    assert out["sample_errors"] == []
    assert out["stopped_reason"] is None
    assert len(flash_batches) == 2

    # Provenance split in triage_assessments: 1 decision + 4 flash
    check_conn = sqlite3.connect(str(tmp_settings.db_path))
    by_model = dict(
        check_conn.execute(
            "SELECT model_id, COUNT(*) FROM triage_assessments GROUP BY model_id"
        ).fetchall()
    )
    check_conn.close()
    assert by_model == {
        "models/gemini-decision-1": 1,
        "models/gemini-3.8-flash": 4,
    }

    # Dry run confirms 0 pending remain
    assert main(["--db-path", db_arg, "triage", "--dry-run"]) == 0
    dry_out = json.loads(capsys.readouterr().out)
    assert dry_out["pending_papers"] == 0


def test_cli_triage_force_flash_and_flash_daily_quota(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for idx in range(3):
        seed_paper(
            db_conn,
            f"2611.3000{idx}",
            title=f"Force Flash Paper {idx}",
            abstract=f"Abstract {idx}",
            published_date=f"2026-11-0{idx + 1}",
        )
    db_conn.commit()
    db_conn.close()

    def _forbid_decisions(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("DecisionClient should not be constructed when --force-flash is set")

    class _QuotaFlashClient:
        def __init__(self, settings: Settings, **kwargs: Any) -> None:
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        @property
        def model_name(self) -> str:
            return "models/gemini-3.8-flash"

        def score_abstract_batch(self, **kwargs: Any) -> FlashBatchResult:
            raise DailyQuotaExceededError(
                "429 RESOURCE_EXHAUSTED: GenerateRequestsPerDayPerProjectPerModel"
            )

    monkeypatch.setattr("arxiv_bench.cli.DecisionClient", _forbid_decisions)
    monkeypatch.setattr("arxiv_bench.cli.FlashTriageClient", _QuotaFlashClient)

    rc = main(
        [
            "--db-path",
            str(tmp_settings.db_path),
            "triage",
            "--flash-batch-size",
            "2",
            "--workers",
            "1",
        ]
    )
    assert rc == 2
    out = json.loads(capsys.readouterr().out)
    assert out["backend"] == "flash"
    assert out["stopped_reason"] == "flash_daily_quota_exceeded"
    assert out["fallback_activated"] is False
    assert out["flash_model"] == "models/gemini-3.8-flash"


def test_flash_triage_client_batch_persist_missing_id_and_bisect(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    for aid in ("2611.40001", "2611.40002", "2611.40003", "2611.40004"):
        seed_paper(db_conn, aid, title=f"Paper {aid}", abstract=f"Abstract {aid}")
    db_conn.commit()
    db_conn.close()

    # Verify daily-quota classifier handles generateContent RPD vs RPM quota IDs
    class _Fake429(RuntimeError):
        status_code = 429

    assert is_daily_quota_error(
        _Fake429("RESOURCE_EXHAUSTED: GenerateRequestsPerDayPerProjectPerModel")
    )
    assert not is_daily_quota_error(
        _Fake429("RESOURCE_EXHAUSTED: GenerateRequestsPerMinutePerProjectPerModel")
    )

    rubric = load_rubric_yaml(tmp_settings.triage_rubric_path)

    class _FakeModelsApi:
        def __init__(self) -> None:
            self.calls = 0
            self.saw_no_thinking = False

        def generate_content(self, *, model: str, contents: str, config: Any) -> Any:
            self.calls += 1
            # Test thinking_budget=0 fallback when model rejects thinking config
            if "flash-lite" in model and getattr(config, "thinking_config", None) is not None:
                raise RuntimeError("400 INVALID_ARGUMENT: thinking_budget=0 unsupported")
            if getattr(config, "thinking_config", None) is None:
                self.saw_no_thinking = True

            # Test poison paper bisection
            if "2611.40004" in contents:
                raise PermanentDecisionError("PROHIBITED_CONTENT safety filter", status_code=422)

            items: list[FlashPaperTriageItem] = []
            # Omit 2611.40002 on the first multi-paper call to exercise missing-ID retry
            if "2611.40001" in contents and "2611.40002" in contents:
                items.append(
                    FlashPaperTriageItem(
                        arxiv_id="2611.40001",
                        is_benchmark_prob=0.92,
                        contribution_type="introduces",
                        primary_modality="text_llm",
                        is_bias_religion_prob=0.05,
                    )
                )
            else:
                for aid in ("2611.40001", "2611.40002", "2611.40003"):
                    if aid in contents:
                        items.append(
                            FlashPaperTriageItem(
                                arxiv_id=aid,
                                is_benchmark_prob=0.81,
                                contribution_type="extends",
                                primary_modality="multimodal",
                                is_bias_religion_prob=0.45,
                            )
                        )
            return SimpleNamespace(
                text=FlashBatchTriageResponse(items=items).model_dump_json(),
                usage_metadata=SimpleNamespace(
                    prompt_token_count=650,
                    candidates_token_count=170,
                    thoughts_token_count=0,
                ),
            )

    fake_models = _FakeModelsApi()
    fake_sdk = SimpleNamespace(models=fake_models)

    fc = FlashTriageClient(tmp_settings, model="gemini-3.8-flash", client=fake_sdk)
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        # Batch 1: 2611.40001 + 2611.40002 -> 40002 omitted initially, recovered on retry
        res1 = fc.score_abstract_batch(
            papers=[
                TriagePaperInput("2611.40001", 1, "T1", "A1", ["cs.AI"]),
                TriagePaperInput("2611.40002", 1, "T2", "A2", ["cs.CL"]),
            ],
            rubric_pack=rubric,
            writer=writer,
            run_id="run-flash-test",
        )
        # Batch 2: 2611.40003 + 2611.40004 (poison) -> bisects so 40003 succeeds and 40004 fails permanently
        res2 = fc.score_abstract_batch(
            papers=[
                TriagePaperInput("2611.40003", 1, "T3", "A3", ["cs.CV"]),
                TriagePaperInput("2611.40004", 1, "T4", "A4", ["cs.AI"]),
            ],
            rubric_pack=rubric,
            writer=writer,
            run_id="run-flash-test",
        )
        writer.flush()

    assert set(res1.succeeded_ids) == {"2611.40001", "2611.40002"}
    assert not res1.permanent_failed
    assert not res1.transient_failed

    assert res2.succeeded_ids == ["2611.40003"]
    assert "2611.40004" in res2.permanent_failed
    assert res2.permanent_failed["2611.40004"][0] == 422

    # Check Flash-Lite thinking fallback and cheaper cost calculation
    fc_lite = FlashTriageClient(tmp_settings, model="gemini-3.5-flash-lite", client=fake_sdk)
    res_lite = fc_lite.score_abstract_batch(
        papers=[TriagePaperInput("2611.40003", 1, "T3", "A3", ["cs.CV"])],
        rubric_pack=rubric,
    )
    assert res_lite.succeeded_ids == ["2611.40003"]
    assert fake_models.saw_no_thinking is True
    assert res_lite.estimated_cost_usd < res1.estimated_cost_usd

    # Verify DB rows written: 3 papers x 4 questions = 12 triage_assessments with models/gemini-3.8-flash
    check_conn = sqlite3.connect(str(tmp_settings.db_path))
    assess_cnt = check_conn.execute(
        "SELECT COUNT(*) FROM triage_assessments WHERE model_id = 'models/gemini-3.8-flash'"
    ).fetchone()[0]
    done_cnt = check_conn.execute(
        "SELECT COUNT(*) FROM paper_stage_status WHERE stage = 'triage' AND status = 'done'"
    ).fetchone()[0]
    log_cnt = check_conn.execute(
        "SELECT COUNT(*) FROM api_call_logs WHERE stage = 'triage_flash'"
    ).fetchone()[0]
    check_conn.close()
    assert assess_cnt == 12
    assert done_cnt == 3
    assert log_cnt >= 4


def test_cli_triage_default_flash_keyset_pagination_and_null_dates(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    for idx in range(4):
        seed_paper(
            db_conn,
            f"2611.5000{idx}",
            title=f"Dated Paper {idx}",
            abstract=f"Abstract {idx}",
            published_date="2026-11-05" if idx < 2 else "2026-11-04",
        )
    # Also seed a paper with NULL published_date to verify the tail pass catches it
    db_conn.execute(
        """
        INSERT INTO papers (
            arxiv_id, latest_version_seen, title, abstract, categories_json, published_date
        ) VALUES ('2611.50099', 1, 'Null Date Paper', 'Abstract null date', '["cs.AI"]', NULL)
        """
    )
    db_conn.commit()
    db_conn.close()

    seen: list[str] = []

    def _forbid_decisions(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("DecisionClient should never be used on default flash backend")

    class _CountingFlashClient:
        def __init__(self, settings: Settings, **kwargs: Any) -> None:
            self.retry_429_count = 0
            self.retry_5xx_count = 0
            self.retry_network_count = 0

        @property
        def model_name(self) -> str:
            return "models/gemini-3.8-flash"

        def score_abstract_batch(
            self,
            *,
            papers: list[TriagePaperInput],
            rubric_pack: Any,
            writer: Any,
            run_id: str,
        ) -> FlashBatchResult:
            for p in papers:
                seen.append(p.arxiv_id)
                writer.submit_sql(
                    """
                    INSERT INTO triage_assessments (
                        arxiv_id, paper_version, rubric_id, rubric_version,
                        question_id, model_id, choice_or_bool, probability,
                        distribution_json, assessed_at
                    ) VALUES (?, ?, ?, ?, 'is_benchmark_contribution', 'models/gemini-3.8-flash', 'false', 0.1, '{}', '2026-11-14T00:00:00Z')
                    """,
                    (
                        p.arxiv_id,
                        p.paper_version,
                        rubric_pack.rubric_id,
                        rubric_pack.rubric_version,
                    ),
                )
            return FlashBatchResult(
                succeeded_ids=[p.arxiv_id for p in papers],
                input_tokens=350 * len(papers),
                output_tokens=75 * len(papers),
                estimated_cost_usd=0.0003 * len(papers),
                latency_ms=200,
            )

    monkeypatch.setattr("arxiv_bench.cli.DecisionClient", _forbid_decisions)
    monkeypatch.setattr("arxiv_bench.cli.FlashTriageClient", _CountingFlashClient)

    rc = main(
        [
            "--db-path",
            str(tmp_settings.db_path),
            "triage",
            "--chunk-size",
            "2",
            "--flash-batch-size",
            "2",
            "--workers",
            "1",
        ]
    )
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["backend"] == "flash"
    assert out["succeeded_flash"] == 5
    assert out["succeeded_decisions"] == 0
    assert set(seen) == {"2611.50000", "2611.50001", "2611.50002", "2611.50003", "2611.50099"}
    assert len(seen) == 5
