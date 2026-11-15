"""Unified CLI entrypoint (`arxiv-bench`) for sync, triage, extract, score, search, matrix, and religion."""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tqdm import tqdm

from arxiv_bench.config import DEFAULT_LEGACY_ROOT, Settings
from arxiv_bench.db import SingleWriterQueue, backup_database, connect_db, init_db
from arxiv_bench.decision_client import (
    DECISION_COST_PER_1M_INPUT_USD,
    DailyQuotaExceededError,
    DecisionClient,
    classify_decision_error,
)
from arxiv_bench.extract_client import ExtractionClient
from arxiv_bench.flash_triage import (
    FlashTriageClient,
    TriagePaperInput,
    flash_cost_rates_per_1m,
)
from arxiv_bench.ingest import sync_atom_delta, sync_snapshot
from arxiv_bench.migrate_legacy import migrate_legacy
from arxiv_bench.pdf_storage import PdfStorageManager, decompress_text
from arxiv_bench.query import (
    build_coverage_matrix,
    get_pipeline_status,
    merge_entity_aliases,
    render_matrix,
    render_search_results,
    search_papers,
)
from arxiv_bench.religion import (
    extract_religion_papers,
    generate_bias_targets_analysis,
    generate_daily_update,
    generate_full_reports,
    generate_nonbias_religion_ethics_report,
    generate_talk_facts_summary,
    generate_wider_net_report,
    select_pending_religion_candidates,
)
from arxiv_bench.s2_client import SemanticScholarClient
from arxiv_bench.schemas import load_rubric_yaml


class JsonlFormatter(logging.Formatter):
    """Structured JSONL log formatter for per-run log files."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "ts": datetime.now(UTC).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "msg": record.getMessage(),
            }
        )


def _setup_logging(settings: Settings, run_id: str) -> logging.Logger:
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    log_file = settings.log_dir / f"{datetime.now(UTC).strftime('%Y-%m-%d')}_{run_id}.jsonl"
    logger = logging.getLogger("arxiv_bench")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(JsonlFormatter())
    logger.addHandler(fh)
    return logger


def _current_git_sha(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def _record_run_start(settings: Settings, run_id: str, mode: str) -> None:
    conn = init_db(settings.db_path)
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO pipeline_runs (run_id, mode, started_at, git_sha, status)
            VALUES (?, ?, ?, ?, 'running')
            """,
            (run_id, mode, datetime.now(UTC).isoformat(), _current_git_sha(settings.repo_root)),
        )
        conn.commit()
    finally:
        conn.close()


def _record_run_finish(
    settings: Settings,
    run_id: str,
    status: str,
    summary: dict[str, Any],
) -> None:
    conn = connect_db(settings.db_path)
    try:
        conn.execute(
            """
            UPDATE pipeline_runs
            SET finished_at = ?, status = ?, summary_json = ?
            WHERE run_id = ?
            """,
            (datetime.now(UTC).isoformat(), status, json.dumps(summary), run_id),
        )
        conn.commit()
    finally:
        conn.close()


def _cmd_migrate_legacy(args: argparse.Namespace, settings: Settings) -> int:
    report = migrate_legacy(
        Path(args.legacy_root),
        settings,
        index_gcs=args.index_gcs,
        io_workers=args.workers,
        dry_run=args.dry_run,
    )
    print(json.dumps(report.__dict__, indent=2))
    return 0


def _cmd_sync(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    _record_run_start(settings, run_id, args.mode)
    conn = init_db(settings.db_path)
    try:
        batch_sz = 2000 if (args.snapshot or args.snapshot_path) else 100
        with SingleWriterQueue(
            settings.db_path, batch_size=batch_sz, max_queue_size=max(2000, batch_sz * 2)
        ) as writer:
            if args.snapshot or args.snapshot_path:
                stats = sync_snapshot(
                    settings,
                    writer,
                    snapshot_path=Path(args.snapshot_path) if args.snapshot_path else None,
                    apply_prefilter=not args.no_prefilter,
                    limit=args.limit,
                )
            else:
                stats = sync_atom_delta(
                    conn,
                    writer,
                    lookback_days=args.lookback_days,
                )
        summary = {"run_id": run_id, **stats.__dict__}
        _record_run_finish(settings, run_id, "completed", summary)
        print(json.dumps(summary, indent=2))
        return 0
    finally:
        conn.close()


def _cmd_calibrate(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    _record_run_start(settings, run_id, "calibrate")
    conn = init_db(settings.db_path)
    try:
        rubric = load_rubric_yaml(Path(args.rubric) if args.rubric else settings.triage_rubric_path)
        dc = DecisionClient(settings)
        with SingleWriterQueue(settings.db_path) as writer:
            report = dc.run_calibration(
                conn,
                rubric,
                sample_size=args.sample_size,
                workers=args.workers,
                writer=writer,
                run_id=run_id,
            )
        payload = {
            "run_id": run_id,
            **{k: v for k, v in report.__dict__.items() if k != "threshold_curve"},
            "threshold_curve": [pt.__dict__ for pt in report.threshold_curve],
        }
        _record_run_finish(settings, run_id, "completed", payload)
        print(json.dumps(payload, indent=2))
        return 0
    finally:
        conn.close()


def _cmd_triage(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    logger = logging.getLogger("arxiv_bench")
    conn = init_db(settings.db_path)
    rubric = load_rubric_yaml(Path(args.rubric) if args.rubric else settings.triage_rubric_path)
    pending_where = """
        FROM papers p
        WHERE p.is_withdrawn = 0
          AND p.abstract IS NOT NULL AND p.abstract != ''
          AND NOT EXISTS (
              SELECT 1 FROM triage_assessments t
              WHERE t.arxiv_id = p.arxiv_id
                AND t.paper_version = COALESCE(p.latest_version_seen, 1)
                AND t.rubric_id = ?
                AND t.rubric_version = ?
                AND t.question_id = 'is_benchmark_contribution'
          )
          AND NOT EXISTS (
              SELECT 1 FROM paper_stage_status s
              WHERE s.arxiv_id = p.arxiv_id
                AND s.stage = 'triage'
                AND s.status = 'failed_permanent'
          )
    """
    base_params: list[Any] = [rubric.rubric_id, rubric.rubric_version]

    backend_arg = str(getattr(args, "backend", "flash") or "flash").lower()
    force_flash: bool = bool(getattr(args, "force_flash", False))
    active_backend = "flash" if (force_flash or backend_arg == "flash") else "decisions"
    flash_model: str = getattr(args, "flash_model", None) or settings.flash_model

    if args.dry_run:
        try:
            row = conn.execute(f"SELECT COUNT(*) AS cnt {pending_where}", base_params).fetchone()
            pending_cnt = int(row["cnt"]) if row else 0
            if args.limit is not None:
                pending_cnt = min(pending_cnt, args.limit)
            in_rate, out_rate = flash_cost_rates_per_1m(flash_model)
            est_flash_in = pending_cnt * 358
            est_flash_out = pending_cnt * 75
            est_flash_cost = (est_flash_in / 1_000_000.0) * in_rate + (
                est_flash_out / 1_000_000.0
            ) * out_rate
            if active_backend == "flash":
                payload: dict[str, Any] = {
                    "rubric_id": rubric.rubric_id,
                    "rubric_version": rubric.rubric_version,
                    "backend": "flash",
                    "model": (
                        flash_model
                        if flash_model.startswith("models/")
                        else f"models/{flash_model}"
                    ),
                    "pending_papers": pending_cnt,
                    "estimated_input_tokens": est_flash_in,
                    "estimated_output_tokens": est_flash_out,
                    "estimated_cost_usd": round(est_flash_cost, 2),
                }
            else:
                est_tokens = pending_cnt * 1129
                est_cost = (est_tokens / 1_000_000.0) * DECISION_COST_PER_1M_INPUT_USD
                payload = {
                    "rubric_id": rubric.rubric_id,
                    "rubric_version": rubric.rubric_version,
                    "backend": "decisions",
                    "model": rubric.model or settings.decision_model,
                    "pending_papers": pending_cnt,
                    "estimated_input_tokens": est_tokens,
                    "estimated_cost_usd": round(est_cost, 2),
                    "fallback_to_flash": bool(getattr(args, "fallback_to_flash", True)),
                    "flash_model": flash_model,
                    "estimated_flash_cost_usd": round(est_flash_cost, 2),
                }
            print(json.dumps(payload, indent=2))
            return 0
        finally:
            conn.close()

    _record_run_start(settings, run_id, "triage")
    t_start = time.monotonic()
    chunk_size = max(1, int(getattr(args, "chunk_size", 2000) or 2000))
    max_cost_usd: float | None = getattr(args, "max_cost_usd", None)
    max_rpm: float | None = getattr(args, "max_rpm", None)
    fallback_to_flash: bool = bool(getattr(args, "fallback_to_flash", True))
    flash_batch_size = max(1, int(getattr(args, "flash_batch_size", 20) or 20))
    raw_flash_workers = getattr(args, "flash_workers", None)
    flash_workers = max(1, int(raw_flash_workers if raw_flash_workers else args.workers))
    raw_flash_max_rpm: float | None = getattr(args, "flash_max_rpm", None)
    flash_max_rpm = (
        raw_flash_max_rpm
        if raw_flash_max_rpm is not None
        else (max_rpm if active_backend == "flash" else None)
    )
    target_limit: int | None = args.limit

    attempted = 0
    succeeded = 0
    succeeded_decisions = 0
    succeeded_flash = 0
    failed_permanent = 0
    failed_transient = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost_usd = 0.0
    stopped_reason: str | None = None
    sample_errors: list[str] = []
    failed_transient_this_run: set[str] = set()
    initial_backend = active_backend
    fallback_activated = False
    fallback_reason: str | None = None

    dc: DecisionClient | None = (
        None
        if active_backend == "flash"
        else (DecisionClient(settings, max_rpm=max_rpm) if max_rpm else DecisionClient(settings))
    )
    fc: FlashTriageClient | None = None
    final_status = "completed"

    def _get_flash_client(*, is_fallback: bool = False) -> FlashTriageClient:
        nonlocal fc
        if fc is None:
            stage_label = "triage_flash_fallback" if is_fallback else "triage_flash"
            kwargs_fc: dict[str, Any] = {"model": flash_model, "stage": stage_label}
            if flash_max_rpm:
                kwargs_fc["max_rpm"] = flash_max_rpm
            fc = FlashTriageClient(settings, **kwargs_fc)
        return fc

    def _record_triage_failure(
        writer: SingleWriterQueue,
        aid: str,
        st_label: str,
        err_code: int,
        err_detail: str,
    ) -> None:
        now_iso = datetime.now(UTC).isoformat()
        writer.submit_sql(
            """
            INSERT INTO paper_stage_status (
                arxiv_id, stage, status, attempt_count,
                last_error_code, last_error_detail, run_id, updated_at
            ) VALUES (?, 'triage', ?, 1, ?, ?, ?, ?)
            ON CONFLICT(arxiv_id, stage) DO UPDATE SET
                status = excluded.status,
                attempt_count = paper_stage_status.attempt_count + 1,
                last_error_code = excluded.last_error_code,
                last_error_detail = excluded.last_error_detail,
                run_id = excluded.run_id,
                updated_at = excluded.updated_at
            """,
            (aid, st_label, str(err_code), err_detail, run_id, now_iso),
        )

    try:
        disable_bar = (not sys.stderr.isatty()) or (os.environ.get("TQDM_DISABLE") == "1")
        chunk_idx = 0
        decisions_daily_quota_hit = False
        flash_daily_quota_hit = False
        cursor: tuple[str, str] | None = None
        null_date_pass = False
        with SingleWriterQueue(settings.db_path, batch_size=300, max_queue_size=8000) as writer:
            with (
                ThreadPoolExecutor(max_workers=max(1, args.workers)) as dec_pool,
                ThreadPoolExecutor(max_workers=flash_workers) as flash_pool,
            ):
                while True:
                    if target_limit is not None:
                        remaining = target_limit - attempted
                        if remaining <= 0:
                            break
                        want = min(chunk_size, remaining)
                    else:
                        want = chunk_size

                    if cursor is not None:
                        cur_pub, cur_aid = cursor
                        extra_where = (
                            " AND p.published_date <= ? "
                            " AND (p.published_date < ? OR (p.published_date = ? AND p.arxiv_id < ?))"
                        )
                        q_params: list[Any] = [
                            *base_params,
                            cur_pub,
                            cur_pub,
                            cur_pub,
                            cur_aid,
                            want,
                        ]
                    elif null_date_pass:
                        extra_where = " AND p.published_date IS NULL"
                        q_params = [*base_params, want + len(failed_transient_this_run)]
                    else:
                        extra_where = ""
                        q_params = [*base_params, want + len(failed_transient_this_run)]

                    rows = conn.execute(
                        f"""
                        SELECT p.arxiv_id, COALESCE(p.latest_version_seen, 1) AS paper_version,
                               p.title, p.abstract, p.categories_json, p.published_date
                        {pending_where}
                        {extra_where}
                        ORDER BY p.published_date DESC, p.arxiv_id DESC
                        LIMIT ?
                        """,
                        q_params,
                    ).fetchall()
                    batch_rows = [
                        r for r in rows if str(r["arxiv_id"]) not in failed_transient_this_run
                    ][:want]
                    if not batch_rows:
                        if cursor is not None:
                            cursor = None
                            null_date_pass = True
                            continue
                        break

                    chunk_idx += 1
                    chunk_backend = active_backend
                    switched_to_flash_this_chunk = False

                    if active_backend == "decisions":
                        assert dc is not None
                        futs = {
                            dec_pool.submit(
                                dc.score_abstract,
                                arxiv_id=str(r["arxiv_id"]),
                                paper_version=int(r["paper_version"]),
                                title=str(r["title"] or ""),
                                abstract=str(r["abstract"] or ""),
                                categories=json.loads(r["categories_json"] or "[]"),
                                rubric_pack=rubric,
                                writer=writer,
                                run_id=run_id,
                            ): str(r["arxiv_id"])
                            for r in batch_rows
                        }
                        quota_err_msg: str | None = None
                        for fut in tqdm(
                            as_completed(futs),
                            total=len(futs),
                            desc=f"Stage 1 triage/decisions (chunk {chunk_idx})",
                            disable=disable_bar,
                        ):
                            aid = futs[fut]
                            if fut.cancelled():
                                continue
                            try:
                                out = fut.result()
                                attempted += 1
                                succeeded += 1
                                succeeded_decisions += 1
                                total_input_tokens += out.input_tokens
                                total_cost_usd += out.estimated_cost_usd
                            except DailyQuotaExceededError as exc:
                                decisions_daily_quota_hit = True
                                quota_err_msg = str(exc)[:300]
                                if not fallback_to_flash:
                                    attempted += 1
                                    failed_transient += 1
                                    failed_transient_this_run.add(aid)
                                    err_msg = f"{aid}: DailyQuotaExceededError: {quota_err_msg}"
                                    if len(sample_errors) < 10 and err_msg not in sample_errors:
                                        sample_errors.append(err_msg)
                                for pending_fut in futs:
                                    pending_fut.cancel()
                            except Exception as exc:  # noqa: BLE001
                                attempted += 1
                                is_perm, err_code, err_detail = classify_decision_error(exc)
                                if is_perm:
                                    failed_permanent += 1
                                    st_label = "failed_permanent"
                                else:
                                    failed_transient += 1
                                    failed_transient_this_run.add(aid)
                                    st_label = "failed_transient"
                                if len(sample_errors) < 10 and err_detail not in sample_errors:
                                    sample_errors.append(f"{aid}: {err_detail}")
                                _record_triage_failure(writer, aid, st_label, err_code, err_detail)

                        writer.flush()
                        if decisions_daily_quota_hit and fallback_to_flash:
                            flash_client = _get_flash_client(is_fallback=True)
                            active_backend = "flash"
                            fallback_activated = True
                            switched_to_flash_this_chunk = True
                            fallback_reason = quota_err_msg
                            fallback_event = {
                                "event": "triage_fallback_activated",
                                "run_id": run_id,
                                "chunk": chunk_idx,
                                "from_model": rubric.model or settings.decision_model,
                                "to_model": flash_client.model_name,
                                "flash_batch_size": flash_batch_size,
                                "flash_workers": flash_workers,
                                "reason": quota_err_msg,
                            }
                            logger.warning(json.dumps(fallback_event))
                            print(json.dumps(fallback_event), file=sys.stderr, flush=True)
                    else:
                        flash_client = _get_flash_client()
                        paper_inputs = [
                            TriagePaperInput(
                                arxiv_id=str(r["arxiv_id"]),
                                paper_version=int(r["paper_version"]),
                                title=str(r["title"] or ""),
                                abstract=str(r["abstract"] or ""),
                                categories=json.loads(r["categories_json"] or "[]"),
                            )
                            for r in batch_rows
                        ]
                        sub_batches = [
                            paper_inputs[i : i + flash_batch_size]
                            for i in range(0, len(paper_inputs), flash_batch_size)
                        ]
                        batch_futs = {
                            flash_pool.submit(
                                flash_client.score_abstract_batch,
                                papers=sb,
                                rubric_pack=rubric,
                                writer=writer,
                                run_id=run_id,
                            ): sb
                            for sb in sub_batches
                        }
                        for bf in tqdm(
                            as_completed(batch_futs),
                            total=len(batch_futs),
                            desc=f"Stage 1 triage/flash (chunk {chunk_idx})",
                            disable=disable_bar,
                        ):
                            sb = batch_futs[bf]
                            if bf.cancelled():
                                continue
                            try:
                                bres = bf.result()
                                total_input_tokens += bres.input_tokens
                                total_output_tokens += bres.output_tokens
                                total_cost_usd += bres.estimated_cost_usd
                                ok_cnt = len(bres.succeeded_ids)
                                attempted += ok_cnt
                                succeeded += ok_cnt
                                succeeded_flash += ok_cnt
                                for aid, (err_code, err_detail) in bres.permanent_failed.items():
                                    attempted += 1
                                    failed_permanent += 1
                                    if len(sample_errors) < 10 and err_detail not in sample_errors:
                                        sample_errors.append(f"{aid}: {err_detail}")
                                    _record_triage_failure(
                                        writer, aid, "failed_permanent", err_code, err_detail
                                    )
                                for aid, (err_code, err_detail) in bres.transient_failed.items():
                                    attempted += 1
                                    failed_transient += 1
                                    failed_transient_this_run.add(aid)
                                    if len(sample_errors) < 10 and err_detail not in sample_errors:
                                        sample_errors.append(f"{aid}: {err_detail}")
                                    _record_triage_failure(
                                        writer, aid, "failed_transient", err_code, err_detail
                                    )
                            except DailyQuotaExceededError as exc:
                                flash_daily_quota_hit = True
                                for p in sb:
                                    attempted += 1
                                    failed_transient += 1
                                    failed_transient_this_run.add(p.arxiv_id)
                                err_msg = f"{sb[0].arxiv_id}: Flash DailyQuotaExceededError: {str(exc)[:300]}"
                                if len(sample_errors) < 10 and err_msg not in sample_errors:
                                    sample_errors.append(err_msg)
                                for pending_bf in batch_futs:
                                    pending_bf.cancel()
                            except Exception as exc:  # noqa: BLE001
                                is_perm, err_code, err_detail = classify_decision_error(exc)
                                for p in sb:
                                    attempted += 1
                                    if is_perm:
                                        failed_permanent += 1
                                        st_label = "failed_permanent"
                                    else:
                                        failed_transient += 1
                                        failed_transient_this_run.add(p.arxiv_id)
                                        st_label = "failed_transient"
                                    _record_triage_failure(
                                        writer, p.arxiv_id, st_label, err_code, err_detail
                                    )
                                if len(sample_errors) < 10 and err_detail not in sample_errors:
                                    sample_errors.append(f"{sb[0].arxiv_id}: {err_detail}")

                        writer.flush()

                    if not switched_to_flash_this_chunk and not null_date_pass and batch_rows:
                        last_row = batch_rows[-1]
                        if last_row["published_date"] is not None:
                            cursor = (str(last_row["published_date"]), str(last_row["arxiv_id"]))
                        else:
                            cursor = None
                            null_date_pass = True

                    elapsed_s = max(1e-6, time.monotonic() - t_start)
                    rpm = succeeded / (elapsed_s / 60.0)
                    tpm = total_input_tokens / (elapsed_s / 60.0)
                    retries_429 = (dc.retry_429_count if dc else 0) + (
                        fc.retry_429_count if fc else 0
                    )
                    retries_5xx = (dc.retry_5xx_count if dc else 0) + (
                        fc.retry_5xx_count if fc else 0
                    )
                    progress = {
                        "event": "triage_chunk_done",
                        "run_id": run_id,
                        "chunk": chunk_idx,
                        "backend": chunk_backend,
                        "attempted": attempted,
                        "succeeded": succeeded,
                        "succeeded_decisions": succeeded_decisions,
                        "succeeded_flash": succeeded_flash,
                        "failed_permanent": failed_permanent,
                        "failed_transient": failed_transient,
                        "retries_429": retries_429,
                        "retries_5xx": retries_5xx,
                        "elapsed_s": round(elapsed_s, 1),
                        "rpm": round(rpm, 1),
                        "tpm": round(tpm, 1),
                        "est_cost_usd": round(total_cost_usd, 4),
                    }
                    logger.info(json.dumps(progress))
                    print(json.dumps(progress), file=sys.stderr, flush=True)

                    if decisions_daily_quota_hit and not fallback_to_flash:
                        stopped_reason = "daily_quota_exceeded"
                        final_status = "stopped_quota"
                        break
                    if flash_daily_quota_hit:
                        stopped_reason = "flash_daily_quota_exceeded"
                        final_status = "stopped_quota"
                        break
                    if max_cost_usd is not None and total_cost_usd >= max_cost_usd:
                        stopped_reason = "max_cost_usd_reached"
                        final_status = "stopped_guard"
                        break
                    if attempted >= 500 and (failed_permanent / attempted) > 0.01:
                        stopped_reason = "permanent_failure_rate_exceeded_1pct"
                        final_status = "stopped_guard"
                        break
                    if (
                        attempted >= 200
                        and ((failed_permanent + failed_transient) / attempted) > 0.10
                    ):
                        stopped_reason = "total_failure_rate_exceeded_10pct"
                        final_status = "stopped_guard"
                        break
    except BaseException:
        final_status = "interrupted"
        raise
    finally:
        conn.close()
        elapsed_s = max(1e-6, time.monotonic() - t_start)
        retries_429_total = (dc.retry_429_count if dc else 0) + (fc.retry_429_count if fc else 0)
        retries_5xx_total = (dc.retry_5xx_count if dc else 0) + (fc.retry_5xx_count if fc else 0)
        retries_net_total = (dc.retry_network_count if dc else 0) + (
            fc.retry_network_count if fc else 0
        )
        summary = {
            "run_id": run_id,
            "backend": (
                "decisions->flash"
                if fallback_activated
                else ("flash" if initial_backend == "flash" else "decisions")
            ),
            "attempted": attempted,
            "succeeded": succeeded,
            "succeeded_decisions": succeeded_decisions,
            "succeeded_flash": succeeded_flash,
            "fallback_activated": fallback_activated,
            "fallback_reason": fallback_reason,
            "flash_model": (
                fc.model_name
                if fc
                else (
                    (flash_model if flash_model.startswith("models/") else f"models/{flash_model}")
                    if initial_backend == "flash"
                    else None
                )
            ),
            "failed": failed_permanent + failed_transient,
            "failed_permanent": failed_permanent,
            "failed_transient": failed_transient,
            "retries_429": retries_429_total,
            "retries_5xx": retries_5xx_total,
            "retries_network": retries_net_total,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "estimated_cost_usd": round(total_cost_usd, 6),
            "elapsed_seconds": round(elapsed_s, 2),
            "observed_rpm": round(succeeded / (elapsed_s / 60.0), 2),
            "observed_tpm": round(total_input_tokens / (elapsed_s / 60.0), 2),
            "stopped_reason": stopped_reason,
            "sample_errors": sample_errors,
        }
        _record_run_finish(settings, run_id, final_status, summary)

    print(json.dumps(summary, indent=2))
    return 0 if stopped_reason is None else 2


def _cmd_extract(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    conn = init_db(settings.db_path)
    storage = PdfStorageManager(settings)
    extractor = ExtractionClient(
        settings,
        storage,
        max_rpm=getattr(args, "max_rpm", None),
        thinking_budget=getattr(args, "thinking_budget", None),
    )
    since = getattr(args, "since", None)
    until = getattr(args, "until", None)
    retry_failed = bool(getattr(args, "retry_failed", False))

    if args.dry_run:
        try:
            est = extractor.estimate_dry_run(
                conn,
                threshold=args.threshold,
                since=since,
                until=until,
                retry_failed=retry_failed,
                limit=args.limit,
            )
            print(json.dumps(est.__dict__, indent=2))
            return 0
        finally:
            conn.close()

    _record_run_start(settings, run_id, "extract")
    final_status = "completed"
    payload: dict[str, Any] = {"run_id": run_id}
    try:
        with SingleWriterQueue(settings.db_path) as writer:
            stats = extractor.run_pending(
                conn,
                writer,
                threshold=args.threshold,
                since=since,
                until=until,
                retry_failed=retry_failed,
                limit=args.limit,
                workers=args.workers,
                chunk_size=max(1, int(getattr(args, "chunk_size", 250) or 250)),
                max_cost_usd=getattr(args, "max_cost_usd", None),
                progress_every=max(0, int(getattr(args, "progress_every", 50) or 0)),
                run_id=run_id,
            )
        if stats.stopped_reason == "daily_quota_exceeded":
            final_status = "stopped_quota"
        elif stats.stopped_reason == "max_cost_usd_reached":
            final_status = "stopped_budget"
        elif stats.stopped_reason is not None:
            final_status = "stopped_guard"
        payload = {"run_id": run_id, **stats.__dict__}
    except BaseException:
        final_status = "interrupted"
        raise
    finally:
        conn.close()
        _record_run_finish(settings, run_id, final_status, payload)

    print(json.dumps(payload, indent=2))
    return 0 if stats.stopped_reason is None else 2


def _cmd_enrich(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    conn = init_db(settings.db_path)
    try:
        s2 = SemanticScholarClient(settings)
        with SingleWriterQueue(settings.db_path) as writer:
            stats = s2.enrich_papers(
                conn,
                writer,
                limit=args.limit,
                stale_days=args.stale_days,
                run_id=run_id,
            )
        print(json.dumps(stats.__dict__, indent=2))
        return 0
    finally:
        conn.close()


def _cmd_score(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    conn = init_db(settings.db_path)
    try:
        rubric = load_rubric_yaml(Path(args.rubric))
        sql = """
            SELECT p.arxiv_id, p.title, p.abstract, p.evidence_card, p.compressed_text_zst
            FROM papers p
            INNER JOIN v_benchmarks vb ON vb.arxiv_id = p.arxiv_id
        """
        params: list[Any] = []
        if args.missing_only:
            sql += """
                WHERE NOT EXISTS (
                    SELECT 1 FROM decision_scores ds
                    WHERE ds.arxiv_id = p.arxiv_id
                      AND ds.rubric_id = ?
                      AND ds.rubric_version = ?
                )
            """
            params.extend([rubric.rubric_id, rubric.rubric_version])
        sql += " ORDER BY p.published_date DESC, p.arxiv_id DESC"
        if args.limit is not None:
            sql += " LIMIT ?"
            params.append(args.limit)
        rows = conn.execute(sql, params).fetchall()

        if args.dry_run:
            est_tokens = len(rows) * (3500 + len(rubric.questions) * 120)
            est_cost = (est_tokens / 1_000_000.0) * DECISION_COST_PER_1M_INPUT_USD
            print(
                json.dumps(
                    {
                        "rubric_id": rubric.rubric_id,
                        "rubric_version": rubric.rubric_version,
                        "questions": len(rubric.questions),
                        "target_papers": len(rows),
                        "estimated_input_tokens": est_tokens,
                        "estimated_cost_usd": round(est_cost, 2),
                    },
                    indent=2,
                )
            )
            return 0

        dc = DecisionClient(settings)
        succeeded = 0
        failed = 0
        disable_bar = not sys.stderr.isatty()
        with SingleWriterQueue(settings.db_path) as writer:
            with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
                futs = {
                    pool.submit(
                        dc.score_rubric_pack,
                        arxiv_id=str(r["arxiv_id"]),
                        title=str(r["title"] or ""),
                        abstract=str(r["abstract"] or ""),
                        evidence_card=str(r["evidence_card"] or ""),
                        body_text=decompress_text(r["compressed_text_zst"]),
                        rubric_pack=rubric,
                        writer=writer,
                        run_id=run_id,
                    ): str(r["arxiv_id"])
                    for r in rows
                }
                for fut in tqdm(
                    as_completed(futs),
                    total=len(futs),
                    desc=f"Scoring {rubric.rubric_id}",
                    disable=disable_bar,
                ):
                    try:
                        fut.result()
                        succeeded += 1
                    except Exception:  # noqa: BLE001
                        failed += 1
            writer.flush()
        print(
            json.dumps({"attempted": len(rows), "succeeded": succeeded, "failed": failed}, indent=2)
        )
        return 0
    finally:
        conn.close()


def _cmd_search(args: argparse.Namespace, settings: Settings) -> int:
    conn = init_db(settings.db_path)
    try:
        r_filter = None
        if args.rubric_filter:
            parts = args.rubric_filter.split(":", 2)
            if len(parts) != 3:
                raise ValueError("--rubric-filter must be formatted as rubric_id:question_id:value")
            r_filter = (parts[0], parts[1], parts[2])
        rows = search_papers(
            conn,
            args.query,
            modality=args.modality,
            domain=args.domain,
            contribution_type=args.contribution_type,
            rubric_filter=r_filter,
            religion_only=args.religion_only,
            limit=args.limit,
        )
        print(render_search_results(rows, fmt=args.format))
        return 0
    finally:
        conn.close()


def _cmd_matrix(args: argparse.Namespace, settings: Settings) -> int:
    conn = init_db(settings.db_path)
    try:
        mat = build_coverage_matrix(
            conn,
            args.rows,
            args.cols,
            domain=args.domain,
            modality=args.modality,
            year_from=args.year_from,
        )
        print(render_matrix(mat, fmt=args.format))
        return 0
    finally:
        conn.close()


def _cmd_alias(args: argparse.Namespace, settings: Settings) -> int:
    conn = init_db(settings.db_path)
    try:
        if args.alias_action == "list":
            rows = conn.execute(
                """
                SELECT e.canonical_id, e.entity_type, e.canonical_name, e.canonical_url,
                       COUNT(a.raw_slug) AS alias_count
                FROM entities e
                LEFT JOIN entity_aliases a ON a.canonical_id = e.canonical_id
                GROUP BY e.canonical_id
                ORDER BY alias_count DESC, e.canonical_id ASC
                LIMIT ?
                """,
                (args.limit,),
            ).fetchall()
            print(json.dumps([dict(r) for r in rows], indent=2))
            return 0
        if args.alias_action == "merge":
            rep = merge_entity_aliases(conn, args.source_id, args.target_id)
            print(json.dumps(rep.__dict__, indent=2))
            return 0
        return 1
    finally:
        conn.close()


def _cmd_status(settings: Settings) -> int:
    conn = init_db(settings.db_path)
    try:
        rep = get_pipeline_status(conn, settings)
        print(json.dumps(rep.__dict__, indent=2))
        return 0
    finally:
        conn.close()


def _cmd_backup(args: argparse.Namespace, settings: Settings) -> int:
    rep = backup_database(
        settings,
        verify_restore=args.verify_restore,
        upload_gcs=not args.no_gcs,
        copy_nfs=not args.no_nfs,
    )
    print(
        json.dumps(
            {
                "timestamp": rep.timestamp,
                "snapshot_bytes": rep.snapshot_bytes,
                "compressed_bytes": rep.compressed_bytes,
                "quick_check_ok": rep.quick_check_ok,
                "restore_verified": rep.restore_verified,
                "local_backup_path": str(rep.local_backup_path) if rep.local_backup_path else None,
                "nfs_backup_path": str(rep.nfs_backup_path) if rep.nfs_backup_path else None,
                "gcs_backup_uri": rep.gcs_backup_uri,
            },
            indent=2,
        )
    )
    return 0


def _cmd_religion(args: argparse.Namespace, settings: Settings, run_id: str) -> int:
    conn = init_db(settings.db_path)
    try:
        storage = PdfStorageManager(settings)
        if args.religion_action == "extract":
            effective_run_id = args.run_id or run_id
            if getattr(args, "dry_run", False):
                cands = select_pending_religion_candidates(
                    conn,
                    threshold=args.threshold,
                    limit=args.limit,
                    since=getattr(args, "since", None),
                    until=getattr(args, "until", None),
                )
                print(
                    json.dumps(
                        {
                            "pending_papers": len(cands),
                            "threshold": args.threshold,
                            "since": getattr(args, "since", None),
                            "until": getattr(args, "until", None),
                            "model": settings.religion_model,
                        },
                        indent=2,
                    )
                )
                return 0
            _record_run_start(settings, effective_run_id, getattr(args, "mode", "daily") or "daily")
            with SingleWriterQueue(settings.db_path) as writer:
                stats = extract_religion_papers(
                    conn,
                    writer,
                    settings,
                    storage,
                    threshold=args.threshold,
                    limit=args.limit,
                    since=getattr(args, "since", None),
                    until=getattr(args, "until", None),
                    workers=max(1, int(getattr(args, "workers", 8) or 8)),
                    run_id=effective_run_id,
                )
            _record_run_finish(settings, effective_run_id, "completed", stats)
            print(json.dumps({"run_id": effective_run_id, **stats}, indent=2))
            return 0
        if args.religion_action == "daily-update":
            out = (
                Path(args.output)
                if args.output
                else settings.repo_root
                / "reports"
                / "daily_updates"
                / f"{datetime.now(UTC).strftime('%Y%m%d')}_daily_update.md"
            )
            cnt = generate_daily_update(conn, args.run_id, out)
            print(
                json.dumps(
                    {"run_id": args.run_id, "papers_written": cnt, "output": str(out)}, indent=2
                )
            )
            return 0
        if args.religion_action == "full-report":
            out_dir = Path(args.output_dir) if args.output_dir else (settings.repo_root / "reports")
            rep = generate_full_reports(conn, out_dir)
            print(json.dumps(rep.__dict__, indent=2))
            return 0
        if args.religion_action == "bias-targets":
            out_dir = Path(args.output_dir) if args.output_dir else (settings.repo_root / "reports")
            path = generate_bias_targets_analysis(conn, out_dir)
            print(json.dumps({"output": str(path)}, indent=2))
            return 0
        if args.religion_action == "non-bias-report":
            out = (
                Path(args.output)
                if args.output
                else settings.repo_root / "reports" / "Non-Bias Religion and Ethics Papers.md"
            )
            cnt = generate_nonbias_religion_ethics_report(conn, out)
            print(json.dumps({"papers_written": cnt, "output": str(out)}, indent=2))
            return 0
        if args.religion_action == "wider-net":
            out = (
                Path(args.output)
                if args.output
                else settings.repo_root / "reports" / "Picked Up with Wider Net.md"
            )
            cnt = generate_wider_net_report(conn, out)
            print(json.dumps({"papers_written": cnt, "output": str(out)}, indent=2))
            return 0
        if args.religion_action == "talk-facts":
            out = (
                Path(args.output)
                if args.output
                else settings.repo_root
                / "reports"
                / "Religious Bias Papers - Interesting Findings.md"
            )
            cnt = generate_talk_facts_summary(
                conn, storage, out, months=args.months, limit=args.limit
            )
            print(json.dumps({"entries_written": cnt, "output": str(out)}, indent=2))
            return 0
        return 1
    finally:
        conn.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arxiv-bench",
        description="All-arXiv AI benchmark corpus pipeline and exploratory gap-analysis CLI.",
    )
    parser.add_argument(
        "--db-path", help="Override SQLite DB path (must be on local NVMe, never NFS)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_mig = sub.add_parser(
        "migrate-legacy", help="Idempotently import legacy NFS CSV/JSON read-only."
    )
    p_mig.add_argument("--legacy-root", default=str(DEFAULT_LEGACY_ROOT))
    p_mig.add_argument(
        "--index-gcs", action="store_true", help="Also index gs://inversion/pdf/ URIs."
    )
    p_mig.add_argument("--workers", type=int, default=16)
    p_mig.add_argument("--dry-run", action="store_true")

    p_sync = sub.add_parser("sync", help="Sync arXiv weekly snapshot or daily Atom delta.")
    p_sync.add_argument("--mode", choices=["daily", "backfill"], default="daily")
    p_sync.add_argument(
        "--snapshot", action="store_true", help="Download weekly snapshot from gs://arxiv-dataset."
    )
    p_sync.add_argument(
        "--snapshot-path", help="Read local JSONL snapshot file instead of downloading."
    )
    p_sync.add_argument("--lookback-days", type=int)
    p_sync.add_argument("--no-prefilter", action="store_true")
    p_sync.add_argument("--limit", type=int)
    p_sync.add_argument("--run-id")

    p_cal = sub.add_parser(
        "calibrate", help="Run Stage 0 200-500 paper gemini-decision-1 calibration gate."
    )
    p_cal.add_argument("--rubric", help="Path to Stage 1 YAML rubric.")
    p_cal.add_argument("--sample-size", type=int, default=300)
    p_cal.add_argument("--workers", type=int, default=8)

    p_tri = sub.add_parser(
        "triage",
        help="Run Stage 1 abstract triage (default: batched gemini-3.8-flash; optional: --backend decisions).",
    )
    p_tri.add_argument("--rubric")
    p_tri.add_argument(
        "--backend",
        choices=["flash", "decisions"],
        default="flash",
        help="Stage 1 triage backend (default: flash using gemini-3.8-flash).",
    )
    p_tri.add_argument("--limit", type=int)
    p_tri.add_argument("--workers", type=int, default=16)
    p_tri.add_argument("--chunk-size", type=int, default=2000)
    p_tri.add_argument("--max-cost-usd", type=float)
    p_tri.add_argument("--max-rpm", type=float)
    p_tri.add_argument(
        "--fallback-to-flash",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When --backend decisions is used, automatically fall back to Gemini Flash if daily quota is exhausted.",
    )
    p_tri.add_argument(
        "--force-flash",
        action="store_true",
        help="Alias for --backend flash.",
    )
    p_tri.add_argument(
        "--flash-model",
        help="Override Gemini Flash model used for Stage 1 triage (defaults to ARXIV_BENCH_FLASH_MODEL / gemini-3.8-flash).",
    )
    p_tri.add_argument("--flash-batch-size", type=int, default=20)
    p_tri.add_argument(
        "--flash-workers",
        type=int,
        help="Override Flash worker threads (defaults to --workers).",
    )
    p_tri.add_argument("--flash-max-rpm", type=float)
    p_tri.add_argument("--dry-run", action="store_true")
    p_tri.add_argument("--run-id")

    p_ext = sub.add_parser(
        "extract", help="Run Stage 2 unified interactive inline-PDF Gemini Flash extraction."
    )
    p_ext.add_argument("--threshold", type=float, default=0.50)
    p_ext.add_argument("--since", help="Only extract papers with published_date >= YYYY-MM-DD.")
    p_ext.add_argument("--until", help="Only extract papers with published_date <= YYYY-MM-DD.")
    p_ext.add_argument(
        "--retry-failed",
        action="store_true",
        help="Also retry papers whose prior Stage 2 status is 'failed'.",
    )
    p_ext.add_argument("--limit", type=int)
    p_ext.add_argument("--workers", type=int, default=8)
    p_ext.add_argument("--chunk-size", type=int, default=250)
    p_ext.add_argument("--max-rpm", type=float)
    p_ext.add_argument("--max-cost-usd", type=float)
    p_ext.add_argument(
        "--thinking-budget",
        type=int,
        help="Optional Gemini thinking token budget (e.g. 0 to disable thinking tokens).",
    )
    p_ext.add_argument("--progress-every", type=int, default=50)
    p_ext.add_argument("--dry-run", action="store_true")
    p_ext.add_argument("--run-id")

    p_enr = sub.add_parser(
        "enrich", help="Run Semantic Scholar 500/call Batch Graph API citation/venue sync."
    )
    p_enr.add_argument("--limit", type=int)
    p_enr.add_argument("--stale-days", type=int, default=30)
    p_enr.add_argument("--run-id")

    p_scr = sub.add_parser(
        "score", help="Run Stage 3 gemini-decision-1 gap-rubric sweep over Evidence Cards."
    )
    p_scr.add_argument("--rubric", required=True)
    p_scr.add_argument("--missing-only", action="store_true", default=True)
    p_scr.add_argument("--all", dest="missing_only", action="store_false")
    p_scr.add_argument("--limit", type=int)
    p_scr.add_argument("--workers", type=int, default=16)
    p_scr.add_argument("--dry-run", action="store_true")
    p_scr.add_argument("--run-id")

    p_srch = sub.add_parser(
        "search", help="Sanitized FTS5 full-text search across benchmarks and religion papers."
    )
    p_srch.add_argument("query")
    p_srch.add_argument("--modality")
    p_srch.add_argument("--domain")
    p_srch.add_argument("--contribution-type")
    p_srch.add_argument("--rubric-filter", help="Filter as rubric_id:question_id:choice_value")
    p_srch.add_argument("--religion-only", action="store_true")
    p_srch.add_argument("--limit", type=int, default=25)
    p_srch.add_argument(
        "--format", choices=["table", "csv", "json", "md", "bibtex"], default="table"
    )

    p_mat = sub.add_parser(
        "matrix", help="Cross-tabulate two benchmark dimensions to spot coverage gaps."
    )
    p_mat.add_argument("--rows", required=True)
    p_mat.add_argument("--cols", required=True)
    p_mat.add_argument("--domain")
    p_mat.add_argument("--modality")
    p_mat.add_argument("--year-from", type=int)
    p_mat.add_argument("--format", choices=["table", "csv", "json", "md"], default="table")

    p_alias = sub.add_parser(
        "alias", help="Inspect or manually merge deterministic entity aliases."
    )
    alias_sub = p_alias.add_subparsers(dest="alias_action", required=True)
    p_al_list = alias_sub.add_parser("list")
    p_al_list.add_argument("--limit", type=int, default=50)
    p_al_merge = alias_sub.add_parser("merge")
    p_al_merge.add_argument("source_id")
    p_al_merge.add_argument("target_id")

    sub.add_parser(
        "status", help="Show pipeline counts, watermark lag alerts, and NVMe/backup health."
    )

    p_bak = sub.add_parser("backup", help="Create online VACUUM INTO + zstd backup to GCS and NFS.")
    p_bak.add_argument("--verify-restore", action="store_true")
    p_bak.add_argument("--no-gcs", action="store_true")
    p_bak.add_argument("--no-nfs", action="store_true")

    p_rel = sub.add_parser("religion", help="Preserved downstream religious-bias module.")
    rel_sub = p_rel.add_subparsers(dest="religion_action", required=True)
    p_re = rel_sub.add_parser("extract")
    p_re.add_argument("--threshold", type=float, default=0.40)
    p_re.add_argument("--limit", type=int)
    p_re.add_argument("--since", help="Only extract papers with published_date >= YYYY-MM-DD.")
    p_re.add_argument("--until", help="Only extract papers with published_date <= YYYY-MM-DD.")
    p_re.add_argument("--workers", type=int, default=8)
    p_re.add_argument("--mode", choices=["daily", "backfill"], default="daily")
    p_re.add_argument("--dry-run", action="store_true")
    p_re.add_argument("--run-id")

    p_rdu = rel_sub.add_parser("daily-update")
    p_rdu.add_argument("--run-id", required=True)
    p_rdu.add_argument("--output")

    p_rfr = rel_sub.add_parser("full-report")
    p_rfr.add_argument("--output-dir")

    p_rbt = rel_sub.add_parser("bias-targets")
    p_rbt.add_argument("--output-dir")

    p_rnb = rel_sub.add_parser("non-bias-report")
    p_rnb.add_argument("--output")

    p_rwn = rel_sub.add_parser("wider-net")
    p_rwn.add_argument("--output")

    p_rtf = rel_sub.add_parser("talk-facts")
    p_rtf.add_argument("--output")
    p_rtf.add_argument("--months", type=int, default=24)
    p_rtf.add_argument("--limit", type=int, default=40)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    settings = Settings.load()
    if args.db_path:
        settings = Settings(**{**settings.__dict__, "db_path": Path(args.db_path).expanduser()})

    run_id = getattr(args, "run_id", None) or uuid.uuid4().hex[:12]
    _setup_logging(settings, run_id)

    cmd = args.command
    if cmd == "migrate-legacy":
        return _cmd_migrate_legacy(args, settings)
    if cmd == "sync":
        return _cmd_sync(args, settings, run_id)
    if cmd == "calibrate":
        return _cmd_calibrate(args, settings, run_id)
    if cmd == "triage":
        return _cmd_triage(args, settings, run_id)
    if cmd == "extract":
        return _cmd_extract(args, settings, run_id)
    if cmd == "enrich":
        return _cmd_enrich(args, settings, run_id)
    if cmd == "score":
        return _cmd_score(args, settings, run_id)
    if cmd == "search":
        return _cmd_search(args, settings)
    if cmd == "matrix":
        return _cmd_matrix(args, settings)
    if cmd == "alias":
        return _cmd_alias(args, settings)
    if cmd == "status":
        return _cmd_status(settings)
    if cmd == "backup":
        return _cmd_backup(args, settings)
    if cmd == "religion":
        return _cmd_religion(args, settings, run_id)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
