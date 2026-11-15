"""Unit tests for snapshot ingestion, Atom delta watermarks, version drift, and Stage 0 pre-filter."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from arxiv_bench.config import Settings, normalize_published_date
from arxiv_bench.db import SingleWriterQueue
from arxiv_bench.ingest import (
    passes_stage0_prefilter,
    sync_atom_delta,
    sync_snapshot,
)


def test_stage0_prefilter_recall_and_precision() -> None:
    # 100% pass for core AI categories
    assert passes_stage0_prefilter(["cs.CL"], "Any Title", "Any abstract") is True
    assert passes_stage0_prefilter(["stat.ML"], "Theory", "No benchmark mention") is True
    assert passes_stage0_prefilter(["eess.AS"], "Speech", "Acoustic features") is True

    # Non-CS rescue requires both AI/ML term and benchmark/dataset/evaluation term
    assert (
        passes_stage0_prefilter(
            ["q-bio.QM"],
            "ProteinBench: Evaluating Large Language Models on Protein Folding",
            "We introduce a benchmark dataset for deep learning protein models.",
        )
        is True
    )
    # Pure physics/math without AI + benchmark terms rejected
    assert (
        passes_stage0_prefilter(
            ["hep-th"],
            "String Theory Compactifications",
            "We derive analytic solutions for Calabi-Yau manifolds.",
        )
        is False
    )
    assert (
        passes_stage0_prefilter(
            ["physics.soc-ph"],
            "Traffic Flow Measurements",
            "We collect a highway sensor dataset for classical differential equations.",
        )
        is False
    )


def test_sync_snapshot_quarantines_truncated_lines_and_tracks_version_drift(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    snap1 = tmp_path / "snap1.jsonl"
    rec_v1 = {
        "id": "2601.00578",
        "title": "BenchMark Alpha",
        "abstract": "We introduce BenchMark Alpha for LLM reasoning.",
        "categories": "cs.AI cs.CL",
        "update_date": "2026-01-05",
        "versions": [{"version": "v1", "created": "Mon, 5 Jan 2026 10:00:00 GMT"}],
    }
    rec_non_ai = {
        "id": "2601.00579",
        "title": "Quantum Hall Effect",
        "abstract": "Topological invariants in condensed matter.",
        "categories": "cond-mat.mes-hall",
        "update_date": "2026-01-05",
        "versions": [{"version": "v1"}],
    }
    # Intentionally append truncated JSON line like the real 2026-01-05 snapshot
    snap1.write_text(
        json.dumps(rec_v1)
        + "\n"
        + json.dumps(rec_non_ai)
        + "\n"
        + '{"id": "2601.00580", "title": "Trunc',
        encoding="utf-8",
    )

    with SingleWriterQueue(tmp_settings.db_path) as writer:
        stats1 = sync_snapshot(tmp_settings, writer, snapshot_path=snap1)

    assert stats1.records_read == 3
    assert stats1.malformed_lines == 1
    assert stats1.prefilter_passed == 1
    assert stats1.records_upserted == 1
    assert stats1.watermark_date == "2026-01-05"

    cp = db_conn.execute(
        "SELECT * FROM ingestion_checkpoints WHERE source = 'arxiv_snapshot_v5'"
    ).fetchone()
    assert cp is not None
    assert int(cp["malformed_lines"]) == 1

    # Now ingest v2 of the same paper with modified abstract -> version_drift must flip to 1
    snap2 = tmp_path / "snap2.jsonl"
    rec_v2 = {
        **rec_v1,
        "abstract": "Updated camera-ready BenchMark Alpha with 50 new tasks.",
        "update_date": "2026-03-10",
        "versions": [
            {"version": "v1", "created": "Mon, 5 Jan 2026 10:00:00 GMT"},
            {"version": "v2", "created": "Tue, 10 Mar 2026 12:00:00 GMT"},
        ],
    }
    snap2.write_text(json.dumps(rec_v2) + "\n", encoding="utf-8")

    with SingleWriterQueue(tmp_settings.db_path) as writer:
        sync_snapshot(tmp_settings, writer, snapshot_path=snap2)

    row = db_conn.execute("SELECT * FROM papers WHERE arxiv_id = '2601.00578'").fetchone()
    assert int(row["latest_version_seen"]) == 2
    assert int(row["version_drift"]) == 1
    assert "50 new tasks" in row["abstract"]


class _FakeAtomResponse:
    def __init__(self, text: str, status_code: int = 200) -> None:
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class _FakeAtomSession:
    def __init__(self, pages: list[str]) -> None:
        self._pages = pages
        self.calls = 0

    def get(
        self, url: str, params: dict[str, Any], headers: dict[str, str], timeout: int
    ) -> _FakeAtomResponse:
        idx = min(self.calls, len(self._pages) - 1)
        self.calls += 1
        return _FakeAtomResponse(self._pages[idx])


def _atom_xml(total: int, entries: list[tuple[str, str, str]]) -> str:
    body = []
    for aid, title, cat in entries:
        body.append(
            f"""
            <entry>
              <id>http://arxiv.org/abs/{aid}v1</id>
              <published>2026-11-12T10:00:00Z</published>
              <updated>2026-11-12T12:00:00Z</updated>
              <title>{title}</title>
              <summary>We introduce a benchmark for AI agents.</summary>
              <category term="{cat}"/>
            </entry>
            """
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
        f"<opensearch:totalResults>{total}</opensearch:totalResults>" + "".join(body) + "</feed>"
    )


def test_sync_atom_delta_verifies_pagination_and_watermark(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
) -> None:
    # Complete run: totalResults=1, 1 entry returned -> watermark advances
    complete_xml = _atom_xml(1, [("2611.00101", "AgentEval Suite", "cs.AI")])
    sess_ok = _FakeAtomSession([complete_xml])
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        stats_ok = sync_atom_delta(
            db_conn,
            writer,
            queries=("cat:cs.AI",),
            delay_seconds=0.0,
            session=sess_ok,  # type: ignore[arg-type]
            now_utc=datetime(2026, 11, 13, 12, 0, tzinfo=UTC),
        )
    assert stats_ok.incomplete_pagination is False
    assert stats_ok.records_upserted == 1
    assert stats_ok.watermark_date == "2026-11-12"

    # Incomplete pagination: totalResults=10, but page 1 returns 1 and page 2 returns 0 -> watermark preserved!
    inc_p1 = _atom_xml(10, [("2611.00102", "Partial Paper", "cs.AI")])
    inc_p2 = _atom_xml(10, [])
    sess_bad = _FakeAtomSession([inc_p1, inc_p2])
    with SingleWriterQueue(tmp_settings.db_path) as writer:
        stats_bad = sync_atom_delta(
            db_conn,
            writer,
            queries=("cat:cs.AI",),
            delay_seconds=0.0,
            session=sess_bad,  # type: ignore[arg-type]
            now_utc=datetime(2026, 11, 13, 18, 0, tzinfo=UTC),
        )
    assert stats_bad.incomplete_pagination is True
    cp = db_conn.execute(
        "SELECT watermark_date, cursor_state FROM ingestion_checkpoints WHERE source = 'arxiv_atom_delta'"
    ).fetchone()
    assert cp["watermark_date"] == "2026-11-12"
    assert cp["cursor_state"] == "incomplete_pagination"


def test_normalize_published_date_and_snapshot_repairs_legacy_garbage(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    assert normalize_published_date("2026-11-12") == "2026-11-12"
    assert normalize_published_date("2026-11-12T18:30:00Z") == "2026-11-12"
    for bad in ("N/A", "Unknown", "null", "XXXX-XX-XX", "2022-XX-XX", "2011-MM-DD", "2026-02-30"):
        assert normalize_published_date(bad) is None
    assert (
        normalize_published_date("N/A", arxiv_id="2512.18979", fallback_to_id=True) == "2025-12-01"
    )
    assert (
        normalize_published_date("Unknown", arxiv_id="cs/0311046", fallback_to_id=True)
        == "2003-11-01"
    )

    # Seed a legacy paper with garbage published_date and verify snapshot upsert repairs it
    db_conn.execute(
        "INSERT INTO papers (arxiv_id, title, published_date) VALUES ('2512.18979', 'Old', 'XXXX-XX-XX')"
    )
    db_conn.execute(
        "INSERT INTO papers (arxiv_id, title, published_date) VALUES ('2512.18980', 'Good', '2025-12-10')"
    )
    db_conn.commit()

    snap = tmp_path / "repair.jsonl"
    recs = [
        {
            "id": "2512.18979",
            "title": "Repaired Paper",
            "abstract": "AI benchmark abstract",
            "categories": "cs.AI",
            "update_date": "2025-12-22",
            "versions": [{"version": "v1", "created": "Mon, 22 Dec 2025 10:00:00 GMT"}],
        },
        {
            "id": "2512.18980",
            "title": "Good Date Preserved",
            "abstract": "AI benchmark abstract",
            "categories": "cs.AI",
            "update_date": "2025-12-25",
            "versions": [{"version": "v1", "created": "Thu, 25 Dec 2025 10:00:00 GMT"}],
        },
    ]
    snap.write_text("\n".join(json.dumps(r) for r in recs) + "\n", encoding="utf-8")

    with SingleWriterQueue(tmp_settings.db_path) as writer:
        sync_snapshot(tmp_settings, writer, snapshot_path=snap)

    repaired = db_conn.execute(
        "SELECT published_date FROM papers WHERE arxiv_id = '2512.18979'"
    ).fetchone()
    preserved = db_conn.execute(
        "SELECT published_date FROM papers WHERE arxiv_id = '2512.18980'"
    ).fetchone()
    assert repaired["published_date"] == "2025-12-22"
    assert preserved["published_date"] == "2025-12-10"
