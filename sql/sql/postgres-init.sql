CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE,
    title VARCHAR(1024),
    content TEXT,
    content_type VARCHAR(128),
    metadata JSONB,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE,
    name VARCHAR(512) NOT NULL,
    entity_type VARCHAR(128),
    description TEXT,
    properties JSONB,
    embedding vector(384),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relationships (
    id SERIAL PRIMARY KEY,
    source_uuid VARCHAR(36),
    target_uuid VARCHAR(36),
    relation_type VARCHAR(128),
    weight FLOAT DEFAULT 1.0,
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_entities_name ON entities USING gin(name gin_trgm_ops);
CREATE INDEX idx_docs_embedding ON documents USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_entities_embedding ON entities USING ivfflat (embedding vector_cosine_ops);
