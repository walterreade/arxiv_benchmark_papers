-- Initial SQLite schema for arxiv-bench (WAL mode, normalized facets + FTS5 + versioned decision scores)

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TEXT NOT NULL
);

-- Core paper record keyed by canonical unversioned arXiv ID (e.g. '2601.15755' or 'cs/0311046')
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    latest_version_seen INTEGER,
    extracted_version INTEGER,
    is_withdrawn INTEGER NOT NULL DEFAULT 0,
    version_drift INTEGER NOT NULL DEFAULT 0,
    title TEXT,
    abstract TEXT,
    categories_json TEXT,
    published_date TEXT,
    updated_date TEXT,
    metadata_sha256 TEXT,
    page_count INTEGER,
    compressed_text_zst BLOB,
    chars_per_page REAL,
    gcs_pdf_uri TEXT,
    pdf_sha256 TEXT,
    pdf_sync_status TEXT,
    extraction_json TEXT,
    evidence_card TEXT,
    stated_limitations TEXT,
    extraction_schema_version TEXT,
    legacy_metadata_json TEXT,
    citation_count INTEGER,
    influential_citation_count INTEGER,
    venue TEXT,
    s2_paper_id TEXT,
    s2_fetched_at TEXT,
    s2_last_error TEXT
);

-- Versioned Stage 1 abstract triage assessments (gemini-decision-1 or imported legacy_llm_bias_v1)
CREATE TABLE IF NOT EXISTS triage_assessments (
    arxiv_id TEXT NOT NULL,
    paper_version INTEGER NOT NULL DEFAULT 0,
    rubric_id TEXT NOT NULL,
    rubric_version TEXT NOT NULL,
    question_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    choice_or_bool TEXT NOT NULL,
    probability REAL NOT NULL,
    distribution_json TEXT,
    assessed_at TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, paper_version, rubric_id, rubric_version, question_id),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

-- Versioned Stage 3 declarative gap-rubric scores (gemini-decision-1)
CREATE TABLE IF NOT EXISTS decision_scores (
    arxiv_id TEXT NOT NULL,
    rubric_id TEXT NOT NULL,
    rubric_version TEXT NOT NULL,
    question_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    choice_or_score TEXT NOT NULL,
    probability REAL NOT NULL,
    entropy REAL NOT NULL DEFAULT 0.0,
    distribution_json TEXT,
    truncated_input INTEGER NOT NULL DEFAULT 0,
    scored_at TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, rubric_id, rubric_version, question_id),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

-- Deterministic entity normalization & alias resolution
CREATE TABLE IF NOT EXISTS entities (
    canonical_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    canonical_name TEXT NOT NULL,
    canonical_url TEXT,
    s2_paper_id TEXT
);

CREATE TABLE IF NOT EXISTS entity_aliases (
    raw_slug TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    canonical_id TEXT NOT NULL,
    resolution_method TEXT NOT NULL,
    PRIMARY KEY (raw_slug, entity_type),
    FOREIGN KEY (canonical_id) REFERENCES entities(canonical_id) ON DELETE CASCADE
);

-- Normalized facet junction tables
CREATE TABLE IF NOT EXISTS paper_benchmarks (
    arxiv_id TEXT NOT NULL,
    canonical_id TEXT NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, canonical_id, role),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE,
    FOREIGN KEY (canonical_id) REFERENCES entities(canonical_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_modalities (
    arxiv_id TEXT NOT NULL,
    modality TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, modality),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_domains (
    arxiv_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, domain),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_tasks (
    arxiv_id TEXT NOT NULL,
    task TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, task),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_models (
    arxiv_id TEXT NOT NULL,
    canonical_id TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, canonical_id),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE,
    FOREIGN KEY (canonical_id) REFERENCES entities(canonical_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_citations (
    citing_arxiv_id TEXT NOT NULL,
    cited_s2_id TEXT NOT NULL,
    cited_arxiv_id TEXT,
    cited_title TEXT,
    PRIMARY KEY (citing_arxiv_id, cited_s2_id),
    FOREIGN KEY (citing_arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

-- External-content FTS5 search index kept synchronized via triggers
CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
    title,
    abstract,
    evidence_card,
    stated_limitations,
    content='papers',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS papers_ai AFTER INSERT ON papers BEGIN
    INSERT INTO papers_fts(rowid, title, abstract, evidence_card, stated_limitations)
    VALUES (new.rowid, new.title, new.abstract, new.evidence_card, new.stated_limitations);
END;

CREATE TRIGGER IF NOT EXISTS papers_ad AFTER DELETE ON papers BEGIN
    INSERT INTO papers_fts(papers_fts, rowid, title, abstract, evidence_card, stated_limitations)
    VALUES ('delete', old.rowid, old.title, old.abstract, old.evidence_card, old.stated_limitations);
END;

CREATE TRIGGER IF NOT EXISTS papers_au AFTER UPDATE ON papers BEGIN
    INSERT INTO papers_fts(papers_fts, rowid, title, abstract, evidence_card, stated_limitations)
    VALUES ('delete', old.rowid, old.title, old.abstract, old.evidence_card, old.stated_limitations);
    INSERT INTO papers_fts(rowid, title, abstract, evidence_card, stated_limitations)
    VALUES (new.rowid, new.title, new.abstract, new.evidence_card, new.stated_limitations);
END;

-- Preserved downstream religious-bias module tables
CREATE TABLE IF NOT EXISTS paper_bias_targets (
    arxiv_id TEXT NOT NULL,
    target TEXT NOT NULL,
    methodology TEXT NOT NULL DEFAULT '',
    is_primary INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (arxiv_id, target, methodology),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS religious_bias_details (
    arxiv_id TEXT PRIMARY KEY,
    religion_component TEXT,
    measurement_description TEXT,
    religious_groups_json TEXT,
    models_tested_json TEXT,
    languages_json TEXT,
    response_type_json TEXT,
    base_benchmarks_json TEXT,
    continuous_testing INTEGER,
    findings TEXT,
    extracted_at TEXT,
    run_id TEXT,
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

-- Operational observability, stage state & ingestion watermarks
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    mode TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    git_sha TEXT,
    status TEXT NOT NULL,
    summary_json TEXT
);

CREATE TABLE IF NOT EXISTS paper_stage_status (
    arxiv_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_error_code TEXT,
    last_error_detail TEXT,
    run_id TEXT,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (arxiv_id, stage),
    FOREIGN KEY (arxiv_id) REFERENCES papers(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ingestion_checkpoints (
    source TEXT PRIMARY KEY,
    watermark_date TEXT,
    cursor_state TEXT,
    malformed_lines INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS api_call_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    stage TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    model TEXT NOT NULL,
    arxiv_id TEXT,
    prompt_tokens INTEGER NOT NULL DEFAULT 0,
    output_tokens INTEGER NOT NULL DEFAULT 0,
    estimated_cost_usd REAL NOT NULL DEFAULT 0.0,
    latency_ms INTEGER NOT NULL DEFAULT 0,
    http_status INTEGER NOT NULL DEFAULT 200,
    created_at TEXT NOT NULL
);

-- Targeted operational and analytical indexes
CREATE INDEX IF NOT EXISTS idx_papers_published_date ON papers(published_date);
CREATE INDEX IF NOT EXISTS idx_papers_pdf_sync_status ON papers(pdf_sync_status);
CREATE INDEX IF NOT EXISTS idx_papers_s2_fetched_at ON papers(s2_fetched_at);
CREATE INDEX IF NOT EXISTS idx_papers_gcs_uri ON papers(gcs_pdf_uri);
CREATE INDEX IF NOT EXISTS idx_triage_lookup ON triage_assessments(rubric_id, rubric_version, question_id, probability);
CREATE INDEX IF NOT EXISTS idx_decision_scores_lookup ON decision_scores(rubric_id, rubric_version, question_id, probability);
CREATE INDEX IF NOT EXISTS idx_stage_status_queue ON paper_stage_status(stage, status);
CREATE INDEX IF NOT EXISTS idx_citations_cited_arxiv ON paper_citations(cited_arxiv_id);
CREATE INDEX IF NOT EXISTS idx_citations_cited_s2 ON paper_citations(cited_s2_id);
CREATE INDEX IF NOT EXISTS idx_entities_type_url ON entities(entity_type, canonical_url);
CREATE INDEX IF NOT EXISTS idx_entities_type_s2 ON entities(entity_type, s2_paper_id);
CREATE INDEX IF NOT EXISTS idx_paper_modalities_mod ON paper_modalities(modality);
CREATE INDEX IF NOT EXISTS idx_paper_domains_dom ON paper_domains(domain);
CREATE INDEX IF NOT EXISTS idx_paper_tasks_task ON paper_tasks(task);
CREATE INDEX IF NOT EXISTS idx_bias_targets_target ON paper_bias_targets(target);

-- Pre-joined read views
CREATE VIEW IF NOT EXISTS v_benchmarks AS
SELECT
    p.arxiv_id,
    p.title,
    p.published_date,
    p.venue,
    p.citation_count,
    p.influential_citation_count,
    p.gcs_pdf_uri,
    p.evidence_card,
    p.stated_limitations,
    json_extract(p.extraction_json, '$.contribution_type') AS contribution_type,
    ta_bench.probability AS triage_benchmark_prob,
    ta_mod.choice_or_bool AS triage_primary_modality
FROM papers p
LEFT JOIN triage_assessments ta_bench
    ON ta_bench.arxiv_id = p.arxiv_id
   AND ta_bench.rubric_id = 'ai_benchmark_triage'
   AND ta_bench.question_id = 'is_benchmark_contribution'
LEFT JOIN triage_assessments ta_mod
    ON ta_mod.arxiv_id = p.arxiv_id
   AND ta_mod.rubric_id = 'ai_benchmark_triage'
   AND ta_mod.question_id = 'primary_modality'
WHERE p.extraction_json IS NOT NULL
  AND COALESCE(json_extract(p.extraction_json, '$.contribution_type'), '') IN (
      'introduces', 'extends', 'audits_critiques', 'surveys'
  );

CREATE VIEW IF NOT EXISTS v_paper_facets AS
SELECT
    p.arxiv_id,
    p.title,
    p.published_date,
    substr(COALESCE(p.published_date, ''), 1, 4) AS pub_year,
    json_extract(p.extraction_json, '$.contribution_type') AS contribution_type,
    pm.modality,
    pd.domain,
    pt.task
FROM papers p
LEFT JOIN paper_modalities pm ON pm.arxiv_id = p.arxiv_id
LEFT JOIN paper_domains pd ON pd.arxiv_id = p.arxiv_id
LEFT JOIN paper_tasks pt ON pt.arxiv_id = p.arxiv_id;

CREATE VIEW IF NOT EXISTS v_religion_papers AS
SELECT
    p.arxiv_id,
    p.title,
    p.published_date,
    p.categories_json,
    p.citation_count,
    p.gcs_pdf_uri,
    r.religion_component,
    r.measurement_description,
    r.religious_groups_json,
    r.models_tested_json,
    r.languages_json,
    r.response_type_json,
    r.base_benchmarks_json,
    r.continuous_testing,
    r.findings,
    r.extracted_at,
    r.run_id
FROM papers p
INNER JOIN religious_bias_details r ON r.arxiv_id = p.arxiv_id;

CREATE VIEW IF NOT EXISTS v_uncertainty_review AS
SELECT
    t.arxiv_id,
    p.title,
    p.published_date,
    t.rubric_id,
    t.rubric_version,
    t.question_id,
    t.choice_or_bool,
    t.probability,
    t.assessed_at
FROM triage_assessments t
INNER JOIN papers p ON p.arxiv_id = t.arxiv_id
WHERE t.probability BETWEEN 0.30 AND 0.70
ORDER BY abs(t.probability - 0.50) ASC;
