"""SQLite connection factory, NFS mount guard, single-writer queue, and atomic backups."""

from __future__ import annotations

import os
import queue
import shutil
import sqlite3
import tempfile
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import zstandard as zstd

from arxiv_bench.config import Settings

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
NFS_FS_TYPES = frozenset({"nfs", "nfs4", "nfs3", "autofs"})


class UnsafeFilesystemError(RuntimeError):
    """Raised when SQLite is pointed at an NFS mount with unsafe advisory locking."""


def _parse_proc_mounts(mounts_text: str) -> list[tuple[str, str]]:
    """Return list of (mount_point, fs_type) pairs from /proc/mounts content."""
    entries: list[tuple[str, str]] = []
    for line in mounts_text.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            mount_point = parts[1].replace("\\040", " ")
            fs_type = parts[2].lower()
            entries.append((mount_point, fs_type))
    return entries


def detect_mount_fstype(
    path: Path,
    mounts_file: Path = Path("/proc/mounts"),
) -> tuple[str | None, str | None]:
    """Return (mount_point, fs_type) for the longest matching mount prefix of realpath(path)."""
    resolved = os.path.realpath(str(path.expanduser()))
    if not mounts_file.exists():
        return None, None
    entries = _parse_proc_mounts(mounts_file.read_text(encoding="utf-8", errors="replace"))
    best_mount: str | None = None
    best_fstype: str | None = None
    for mount_point, fs_type in entries:
        normalized_mp = mount_point.rstrip("/") or "/"
        if normalized_mp == "/":
            matches = True
        else:
            matches = resolved == normalized_mp or resolved.startswith(normalized_mp + "/")
        if matches and (best_mount is None or len(normalized_mp) > len(best_mount)):
            best_mount = normalized_mp
            best_fstype = fs_type
    return best_mount, best_fstype


def assert_not_nfs(db_path: Path, mounts_file: Path = Path("/proc/mounts")) -> None:
    """Refuse to open SQLite on NFS mounts where local_lock=none corrupts WAL databases."""
    probe_target = db_path if db_path.exists() else db_path.parent
    # Walk upward until an existing directory is found so realpath resolves symlinks accurately
    while not probe_target.exists() and probe_target != probe_target.parent:
        probe_target = probe_target.parent

    mount_point, fs_type = detect_mount_fstype(probe_target, mounts_file=mounts_file)
    if fs_type in NFS_FS_TYPES:
        raise UnsafeFilesystemError(
            f"Refusing to open SQLite database '{db_path}' on NFS mount '{mount_point}' "
            f"(fstype={fs_type}). Move ARXIV_BENCH_DB_PATH onto local NVMe "
            "(for example, ~/.local/share/arxiv_bench/benchmarks.db)."
        )


def connect_db(
    db_path: Path,
    *,
    readonly: bool = False,
    mounts_file: Path = Path("/proc/mounts"),
) -> sqlite3.Connection:
    """Open a WAL-mode SQLite connection after enforcing the NFS mount guard."""
    assert_not_nfs(db_path, mounts_file=mounts_file)
    if not readonly:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), timeout=30.0, check_same_thread=False)
    else:
        uri = f"file:{db_path.resolve()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, timeout=30.0, check_same_thread=False)

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000;")
    conn.execute("PRAGMA foreign_keys=ON;")
    if not readonly:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def apply_migrations(conn: sqlite3.Connection, migrations_dir: Path = MIGRATIONS_DIR) -> list[str]:
    """Apply pending ordered SQL migration scripts and return newly applied version names."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations "
        "(version TEXT PRIMARY KEY, applied_at TEXT NOT NULL)"
    )
    applied = {
        row["version"] for row in conn.execute("SELECT version FROM schema_migrations").fetchall()
    }
    newly_applied: list[str] = []
    for sql_file in sorted(migrations_dir.glob("*.sql")):
        version = sql_file.stem
        if version in applied:
            continue
        sql_script = sql_file.read_text(encoding="utf-8")
        conn.executescript(sql_script)
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute(
            "INSERT OR IGNORE INTO schema_migrations (version, applied_at) VALUES (?, ?)",
            (version, datetime.now(UTC).isoformat()),
        )
        conn.commit()
        newly_applied.append(version)
    return newly_applied


def init_db(db_path: Path, *, mounts_file: Path = Path("/proc/mounts")) -> sqlite3.Connection:
    """Connect to SQLite on local disk and apply all schema migrations."""
    conn = connect_db(db_path, mounts_file=mounts_file)
    apply_migrations(conn)
    return conn


WriteCallable = Callable[[sqlite3.Cursor], None]


class SingleWriterQueue:
    """Dedicated single-writer SQLite worker committing batches of 50-200 operations."""

    def __init__(
        self,
        db_path: Path,
        *,
        batch_size: int = 100,
        max_queue_size: int = 2000,
        mounts_file: Path = Path("/proc/mounts"),
    ) -> None:
        self._db_path = db_path
        self._batch_size = max(1, batch_size)
        self._mounts_file = mounts_file
        self._queue: queue.Queue[WriteCallable | None] = queue.Queue(maxsize=max_queue_size)
        self._error: BaseException | None = None
        self._committed_ops = 0
        self._thread: threading.Thread | None = None
        self._started = False

    @property
    def committed_ops(self) -> int:
        return self._committed_ops

    def start(self) -> SingleWriterQueue:
        assert_not_nfs(self._db_path, mounts_file=self._mounts_file)
        self._started = True
        self._thread = threading.Thread(
            target=self._run,
            name="arxiv-bench-sqlite-writer",
            daemon=True,
        )
        self._thread.start()
        return self

    def submit(self, fn: WriteCallable) -> None:
        """Enqueue a write operation accepting an sqlite3.Cursor."""
        if self._error is not None:
            raise RuntimeError("SQLite writer thread failed") from self._error
        if not self._started:
            raise RuntimeError("SingleWriterQueue must be started before submitting writes.")
        self._queue.put(fn)

    def submit_sql(self, sql: str, params: tuple[Any, ...] | dict[str, Any] = ()) -> None:
        """Convenience wrapper for enqueueing a single parameterized SQL statement."""
        self.submit(lambda cur: cur.execute(sql, params))

    def flush(self) -> None:
        """Block until all currently queued operations have been committed."""
        done = threading.Event()
        self.submit(lambda _cur: done.set())
        # Force commit boundary by sending a lightweight flush marker and polling error state
        while not done.wait(timeout=0.1):
            if self._error is not None:
                raise RuntimeError("SQLite writer thread failed") from self._error

    def close(self) -> None:
        """Drain remaining writes, commit final batch, and stop writer thread."""
        if not self._started:
            return
        self._queue.put(None)
        if self._thread is not None:
            self._thread.join()
        self._started = False
        if self._error is not None:
            raise RuntimeError("SQLite writer thread failed") from self._error

    def __enter__(self) -> SingleWriterQueue:
        return self.start()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _run(self) -> None:
        conn = connect_db(self._db_path, mounts_file=self._mounts_file)
        try:
            batch: list[WriteCallable] = []
            stop_requested = False
            while not stop_requested:
                try:
                    item = self._queue.get(timeout=0.05)
                except queue.Empty:
                    if batch:
                        self._commit_batch(conn, batch)
                        batch.clear()
                    continue

                if item is None:
                    stop_requested = True
                else:
                    batch.append(item)

                while len(batch) < self._batch_size and not stop_requested:
                    try:
                        nxt = self._queue.get_nowait()
                    except queue.Empty:
                        break
                    if nxt is None:
                        stop_requested = True
                    else:
                        batch.append(nxt)

                if batch:
                    self._commit_batch(conn, batch)
                    batch.clear()
        except BaseException as exc:  # noqa: BLE001
            self._error = exc
        finally:
            conn.close()

    def _commit_batch(self, conn: sqlite3.Connection, batch: list[WriteCallable]) -> None:
        cur = conn.cursor()
        try:
            cur.execute("BEGIN IMMEDIATE;")
            for op in batch:
                op(cur)
            conn.commit()
            self._committed_ops += len(batch)
        except BaseException:
            conn.rollback()
            raise


@dataclass(frozen=True)
class BackupReport:
    """Result summary for an atomic VACUUM INTO + zstd database backup."""

    timestamp: str
    snapshot_bytes: int
    compressed_bytes: int
    quick_check_ok: bool
    restore_verified: bool
    local_backup_path: Path | None
    nfs_backup_path: Path | None
    gcs_backup_uri: str | None


def backup_database(
    settings: Settings,
    *,
    verify_restore: bool = False,
    upload_gcs: bool = True,
    copy_nfs: bool = True,
    gcs_client: Any | None = None,
    keep_last: int = 14,
) -> BackupReport:
    """Create a consistent online VACUUM INTO snapshot, verify, compress with zstd, and replicate."""
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    with tempfile.TemporaryDirectory(prefix="arxiv_bench_backup_") as tmp:
        tmp_dir = Path(tmp)
        snap_path = tmp_dir / f"benchmarks_{ts}.db"
        zst_path = tmp_dir / f"benchmarks_{ts}.db.zst"

        conn = connect_db(settings.db_path)
        try:
            escaped = str(snap_path).replace("'", "''")
            conn.execute(f"VACUUM INTO '{escaped}'")
        finally:
            conn.close()

        # Verify snapshot integrity before compression
        snap_conn = sqlite3.connect(str(snap_path))
        try:
            quick_row = snap_conn.execute("PRAGMA quick_check;").fetchone()
            quick_ok = bool(quick_row and quick_row[0] == "ok")
        finally:
            snap_conn.close()

        if not quick_ok:
            raise RuntimeError(f"VACUUM INTO snapshot failed PRAGMA quick_check: {quick_row}")

        snapshot_bytes = snap_path.stat().st_size
        cctx = zstd.ZstdCompressor(level=6)
        with snap_path.open("rb") as src, zst_path.open("wb") as dst:
            cctx.copy_stream(src, dst)
        compressed_bytes = zst_path.stat().st_size

        restore_verified = False
        if verify_restore:
            restored_path = tmp_dir / "restored.db"
            dctx = zstd.ZstdDecompressor()
            with zst_path.open("rb") as src, restored_path.open("wb") as dst:
                dctx.copy_stream(src, dst)
            rconn = sqlite3.connect(str(restored_path))
            try:
                integ = rconn.execute("PRAGMA integrity_check;").fetchone()
                restore_verified = bool(integ and integ[0] == "ok")
            finally:
                rconn.close()
            if not restore_verified:
                raise RuntimeError(f"Restored backup failed PRAGMA integrity_check: {integ}")

        # Local NVMe rotating backup copy alongside DB directory
        local_dir = settings.db_path.parent / "backups"
        local_dir.mkdir(parents=True, exist_ok=True)
        local_target = local_dir / f"benchmarks_{ts}.db.zst"
        shutil.copy2(zst_path, local_target)
        shutil.copy2(zst_path, local_dir / "latest.db.zst")
        _prune_old_backups(local_dir, keep_last=keep_last)

        nfs_target: Path | None = None
        if copy_nfs and settings.nfs_backup_dir:
            try:
                settings.nfs_backup_dir.mkdir(parents=True, exist_ok=True)
                nfs_target = settings.nfs_backup_dir / f"benchmarks_{ts}.db.zst"
                shutil.copy2(zst_path, nfs_target)
                shutil.copy2(zst_path, settings.nfs_backup_dir / "latest.db.zst")
                _prune_old_backups(settings.nfs_backup_dir, keep_last=keep_last)
            except OSError:
                nfs_target = None

        gcs_uri: str | None = None
        if upload_gcs and settings.gcs_archive_bucket:
            client = gcs_client
            if client is None:
                from google.cloud import storage

                client = storage.Client()
            bucket = client.bucket(settings.gcs_archive_bucket)
            ts_blob = bucket.blob(f"backups/sqlite/benchmarks_{ts}.db.zst")
            ts_blob.upload_from_filename(str(zst_path))
            latest_blob = bucket.blob("backups/sqlite/latest.db.zst")
            latest_blob.upload_from_filename(str(zst_path))
            gcs_uri = f"gs://{settings.gcs_archive_bucket}/backups/sqlite/benchmarks_{ts}.db.zst"

        return BackupReport(
            timestamp=ts,
            snapshot_bytes=snapshot_bytes,
            compressed_bytes=compressed_bytes,
            quick_check_ok=quick_ok,
            restore_verified=restore_verified,
            local_backup_path=local_target,
            nfs_backup_path=nfs_target,
            gcs_backup_uri=gcs_uri,
        )


def _prune_old_backups(directory: Path, *, keep_last: int) -> None:
    files = sorted(
        (p for p in directory.glob("benchmarks_*.db.zst") if p.is_file()),
        reverse=True,
    )
    for stale in files[keep_last:]:
        stale.unlink(missing_ok=True)
