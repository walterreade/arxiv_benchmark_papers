"""Unit & concurrency tests for db.py, NFS startup guard, FTS5 triggers, and VACUUM INTO backups."""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path

import pytest

from arxiv_bench.config import Settings
from arxiv_bench.db import (
    SingleWriterQueue,
    UnsafeFilesystemError,
    apply_migrations,
    assert_not_nfs,
    backup_database,
    connect_db,
    init_db,
)
from tests.conftest import FakeGCSClient


def test_wal_pragmas_and_idempotent_migrations(tmp_settings: Settings) -> None:
    conn = init_db(tmp_settings.db_path)
    try:
        mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
        fk = conn.execute("PRAGMA foreign_keys;").fetchone()[0]
        timeout = conn.execute("PRAGMA busy_timeout;").fetchone()[0]
        assert str(mode).lower() == "wal"
        assert int(fk) == 1
        assert int(timeout) == 30000
        # Re-applying migrations must be a no-op
        assert apply_migrations(conn) == []
    finally:
        conn.close()


def test_nfs_mount_guard_blocks_nfs_and_symlinks(tmp_path: Path) -> None:
    nfs_dir = tmp_path / "mnt_filestore"
    nfs_dir.mkdir()
    local_dir = tmp_path / "local_nvme"
    local_dir.mkdir()
    symlink_to_nfs = tmp_path / "link_to_nfs"
    symlink_to_nfs.symlink_to(nfs_dir)

    mounts = tmp_path / "proc_mounts"
    mounts.write_text(
        f"/dev/nvme0n1p1 / ext4 rw,relatime 0 0\n"
        f"10.71.148.10:/competitions {nfs_dir} nfs rw,local_lock=none 0 0\n",
        encoding="utf-8",
    )

    # Local path succeeds
    assert_not_nfs(local_dir / "benchmarks.db", mounts_file=mounts)

    # Direct NFS path raises
    with pytest.raises(UnsafeFilesystemError, match="NFS mount"):
        assert_not_nfs(nfs_dir / "benchmarks.db", mounts_file=mounts)

    # Symlink resolving onto NFS also raises
    with pytest.raises(UnsafeFilesystemError, match="NFS mount"):
        assert_not_nfs(symlink_to_nfs / "benchmarks.db", mounts_file=mounts)


def test_single_writer_queue_multithreaded_zero_busy(tmp_settings: Settings) -> None:
    conn = init_db(tmp_settings.db_path)
    conn.close()

    num_threads = 16
    per_thread = 25
    errors: list[BaseException] = []

    with SingleWriterQueue(tmp_settings.db_path, batch_size=50) as writer:

        def _producer(tid: int) -> None:
            try:
                for i in range(per_thread):
                    aid = f"2601.{tid:02d}{i:03d}"
                    writer.submit_sql(
                        "INSERT INTO papers (arxiv_id, title, abstract) VALUES (?, ?, ?)",
                        (aid, f"Paper {aid}", "Synthetic benchmark abstract"),
                    )
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)

        def _reader() -> None:
            rconn = connect_db(tmp_settings.db_path, readonly=True)
            try:
                for _ in range(30):
                    rconn.execute("SELECT COUNT(*) FROM papers").fetchone()
            except BaseException as exc:  # noqa: BLE001
                errors.append(exc)
            finally:
                rconn.close()

        threads = [threading.Thread(target=_producer, args=(t,)) for t in range(num_threads)]
        threads.append(threading.Thread(target=_reader))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    assert not errors
    check_conn = connect_db(tmp_settings.db_path, readonly=True)
    try:
        cnt = int(check_conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0])
        assert cnt == num_threads * per_thread
    finally:
        check_conn.close()


def test_papers_fts_triggers_sync_insert_update_delete(db_conn: sqlite3.Connection) -> None:
    db_conn.execute(
        """
        INSERT INTO papers (arxiv_id, title, abstract, evidence_card, stated_limitations)
        VALUES ('2605.00001', 'SWE-bench Clinical', 'Initial abstract', 'Card alpha', 'Limited English')
        """
    )
    db_conn.commit()
    hits = db_conn.execute(
        "SELECT rowid FROM papers_fts WHERE papers_fts MATCH '\"SWE-bench\"'"
    ).fetchall()
    assert len(hits) == 1

    db_conn.execute(
        "UPDATE papers SET title = 'MedAgentBench v2', stated_limitations = 'No Hindi' WHERE arxiv_id = '2605.00001'"
    )
    db_conn.commit()
    assert (
        db_conn.execute(
            "SELECT rowid FROM papers_fts WHERE papers_fts MATCH '\"SWE-bench\"'"
        ).fetchall()
        == []
    )
    assert (
        len(
            db_conn.execute(
                "SELECT rowid FROM papers_fts WHERE papers_fts MATCH 'Hindi'"
            ).fetchall()
        )
        == 1
    )

    db_conn.execute("DELETE FROM papers WHERE arxiv_id = '2605.00001'")
    db_conn.commit()
    assert (
        db_conn.execute("SELECT rowid FROM papers_fts WHERE papers_fts MATCH 'Hindi'").fetchall()
        == []
    )


def test_backup_database_vacuum_zstd_and_restore_verification(
    tmp_settings: Settings,
    db_conn: sqlite3.Connection,
    fake_gcs: FakeGCSClient,
) -> None:
    db_conn.execute("INSERT INTO papers (arxiv_id, title) VALUES ('2605.12345', 'Backup Test')")
    db_conn.commit()

    rep = backup_database(
        tmp_settings,
        verify_restore=True,
        upload_gcs=True,
        copy_nfs=True,
        gcs_client=fake_gcs,
    )
    assert rep.quick_check_ok is True
    assert rep.restore_verified is True
    assert rep.snapshot_bytes > 0
    assert rep.compressed_bytes > 0
    assert rep.local_backup_path and rep.local_backup_path.exists()
    assert rep.nfs_backup_path and rep.nfs_backup_path.exists()
    assert rep.gcs_backup_uri and rep.gcs_backup_uri.startswith("gs://inversion/backups/sqlite/")
    assert "backups/sqlite/latest.db.zst" in fake_gcs.bucket("inversion").store


def test_optimize_database_populates_sqlite_stat1(db_conn: sqlite3.Connection) -> None:
    from arxiv_bench.db import optimize_database

    db_conn.execute("INSERT INTO papers (arxiv_id, title) VALUES ('2605.99999', 'Stat Test')")
    db_conn.commit()
    optimize_database(db_conn, full_analyze=True)
    stat_rows = db_conn.execute("SELECT tbl FROM sqlite_stat1 WHERE tbl = 'papers'").fetchall()
    assert len(stat_rows) >= 1
