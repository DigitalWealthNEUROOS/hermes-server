CREATE DATABASE IF NOT EXISTS hermes_storage;
CREATE DATABASE IF NOT EXISTS hermes_analytics;
CREATE DATABASE IF NOT EXISTS hermes_sessions;
CREATE DATABASE IF NOT EXISTS hermes_cache;
CREATE DATABASE IF NOT EXISTS nextcloud;

USE hermes_storage;
CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) UNIQUE,
    name VARCHAR(512) NOT NULL,
    size BIGINT,
    storage_backend VARCHAR(32) DEFAULT 'minio',
    bucket VARCHAR(256),
    content_hash VARCHAR(64),
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_uuid (uuid),
    INDEX idx_hash (content_hash)
) ENGINE=InnoDB;

USE hermes_analytics;
CREATE TABLE IF NOT EXISTS agent_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(256) UNIQUE,
    platform VARCHAR(64),
    messages INT DEFAULT 0,
    tokens_in BIGINT DEFAULT 0,
    tokens_out BIGINT DEFAULT 0,
    cost DECIMAL(10,6) DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session (session_id)
) ENGINE=InnoDB;

GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'%' IDENTIFIED BY 'nextcloud_2026';
FLUSH PRIVILEGES;
