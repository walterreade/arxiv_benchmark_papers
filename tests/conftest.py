"""Shared pytest fixtures for local NVMe/tmp SQLite, mock GCS, and synthetic PDFs."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pymupdf
import pytest

from arxiv_bench.config import Settings
from arxiv_bench.db import init_db


class FakeGCSBlob:
    """In-memory GCS blob double supporting upload, download, and existence checks."""

    def __init__(self, bucket: FakeGCSBucket, name: str) -> None:
        self._bucket = bucket
        self.name = name

    def exists(self) -> bool:
        return self.name in self._bucket.store

    def upload_from_filename(self, filename: str, content_type: str | None = None) -> None:
        if self._bucket.fail_uploads_with is not None:
            raise self._bucket.fail_uploads_with
        self._bucket.store[self.name] = Path(filename).read_bytes()

    def download_to_filename(self, filename: str) -> None:
        if self.name not in self._bucket.store:
            raise FileNotFoundError(self.name)
        Path(filename).write_bytes(self._bucket.store[self.name])


class FakeGCSBucket:
    """In-memory GCS bucket double."""

    def __init__(self, name: str, *, fail_uploads_with: Exception | None = None) -> None:
        self.name = name
        self.store: dict[str, bytes] = {}
        self.fail_uploads_with = fail_uploads_with

    def blob(self, blob_name: str) -> FakeGCSBlob:
        return FakeGCSBlob(self, blob_name)


class FakeGCSClient:
    """In-memory GCS client double."""

    def __init__(self, buckets: dict[str, FakeGCSBucket] | None = None) -> None:
        self.buckets: dict[str, FakeGCSBucket] = buckets or {}

    def bucket(self, name: str, user_project: str | None = None) -> FakeGCSBucket:
        if name not in self.buckets:
            self.buckets[name] = FakeGCSBucket(name)
        return self.buckets[name]

    def list_blobs(self, bucket_name: str, prefix: str = "") -> list[FakeGCSBlob]:
        b = self.bucket(bucket_name)
        return [FakeGCSBlob(b, k) for k in sorted(b.store.keys()) if k.startswith(prefix)]


def make_sample_pdf(
    path: Path,
    text: str = "Benchmark Evaluation Paper\n\nSection 1\nBody text.\n\nReferences\n[1] Ref A",
) -> Path:
    """Generate a real valid multi-kilobyte PDF binary using PyMuPDF."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text + ("\n" + "padding " * 120))
    doc.save(str(path))
    doc.close()
    return path


@pytest.fixture
def tmp_settings(tmp_path: Path) -> Settings:
    """Isolated Settings pointing all paths to tmp_path (guaranteed non-NFS)."""
    repo_root = Path(__file__).resolve().parent.parent
    return Settings(
        repo_root=repo_root,
        db_path=tmp_path / "data" / "benchmarks.db",
        staging_dir=tmp_path / "staging",
        log_dir=tmp_path / "logs",
        max_staging_gb=10.0,
        google_api_key="test-google-key",
        s2_api_key="test-s2-key",
        gcs_archive_bucket="inversion",
        gcs_arxiv_bucket="arxiv-dataset",
        gcp_requester_pays_project="test-project",
        nfs_backup_dir=tmp_path / "nfs_backups",
        decision_model="models/gemini-decision-1",
        flash_model="gemini-3.8-flash",
        religion_model="gemini-3.8-flash",
        triage_rubric_path=repo_root / "rubrics" / "stage1_triage_v2.yaml",
    )


@pytest.fixture
def db_conn(tmp_settings: Settings) -> sqlite3.Connection:
    """Migrated SQLite connection on local tmp_path."""
    conn = init_db(tmp_settings.db_path)
    yield conn
    conn.close()


@pytest.fixture
def fake_gcs() -> FakeGCSClient:
    return FakeGCSClient()


@pytest.fixture
def sample_pdf_path(tmp_path: Path) -> Path:
    return make_sample_pdf(tmp_path / "sample.pdf")


def seed_paper(
    conn: sqlite3.Connection,
    arxiv_id: str,
    *,
    title: str = "Test Benchmark Paper",
    abstract: str = "We introduce a new benchmark for AI evaluation.",
    published_date: str = "2026-05-01",
    categories: list[str] | None = None,
    evidence_card: str | None = None,
    stated_limitations: str | None = None,
    extraction_json: str | None = None,
    gcs_pdf_uri: str | None = None,
) -> None:
    import json

    conn.execute(
        """
        INSERT INTO papers (
            arxiv_id, latest_version_seen, title, abstract, categories_json,
            published_date, updated_date, evidence_card, stated_limitations,
            extraction_json, gcs_pdf_uri
        ) VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            arxiv_id,
            title,
            abstract,
            json.dumps(categories or ["cs.AI"]),
            published_date,
            published_date,
            evidence_card,
            stated_limitations,
            extraction_json,
            gcs_pdf_uri,
        ),
    )
    conn.commit()
