-- MAXIMUS Database Schema
-- Created: 2025-11-11

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Decisions table (HITL governance)
CREATE TABLE decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    decision_id VARCHAR(255) UNIQUE NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    requires_approval BOOLEAN DEFAULT TRUE,
    operator_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operator sessions
CREATE TABLE operator_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    operator_id VARCHAR(255) NOT NULL,
    operator_name VARCHAR(255) NOT NULL,
    operator_role VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ESGT events
CREATE TABLE esgt_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    data JSONB NOT NULL,
    arousal_before FLOAT,
    arousal_after FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Healing patches (PENELOPE)
CREATE TABLE healing_patches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_path TEXT NOT NULL,
    patch_content TEXT NOT NULL,
    fruit_type VARCHAR(50),
    confidence FLOAT,
    applied BOOLEAN DEFAULT FALSE,
    applied_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consciousness state snapshots
CREATE TABLE consciousness_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    arousal_level FLOAT NOT NULL,
    arousal_classification VARCHAR(50) NOT NULL,
    esgt_active BOOLEAN NOT NULL,
    system_health VARCHAR(50) NOT NULL,
    tig_metrics JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_decisions_status ON decisions(status);
CREATE INDEX idx_decisions_created ON decisions(created_at DESC);
CREATE INDEX idx_sessions_operator ON operator_sessions(operator_id);
CREATE INDEX idx_esgt_timestamp ON esgt_events(timestamp DESC);
CREATE INDEX idx_consciousness_timestamp ON consciousness_snapshots(timestamp DESC);

-- Views
CREATE VIEW pending_decisions AS
SELECT * FROM decisions
WHERE status = 'pending'
ORDER BY created_at DESC;

CREATE VIEW active_sessions AS
SELECT * FROM operator_sessions
WHERE last_activity > CURRENT_TIMESTAMP - INTERVAL '1 hour'
ORDER BY last_activity DESC;

-- Seed admin user (for testing)
INSERT INTO operator_sessions (session_id, operator_id, operator_name, operator_role)
VALUES ('admin-session-001', 'admin', 'Administrator', 'admin');
