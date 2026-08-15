-- =============================================================================
-- Chitin.ai — Database Schema for CockroachDB Cloud
-- Includes:
--   1. Historical Incident Memory (Distributed Vector Indexing)
--   2. Active Remediation Transactional State
--   3. Agent Execution Audit Trail
--   4. Managed Cluster Inventory
-- =============================================================================

-- Enable required extensions (if applicable on CockroachDB cluster)
-- CockroachDB natively supports VECTOR types and vector indexing out of the box.

-- -----------------------------------------------------------------------------
-- 1. Historical Incident Memory Table (RAG Vector Store)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS historical_incidents (
    incident_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title STRING NOT NULL,
    service_name STRING NOT NULL,
    error_signature STRING NOT NULL,
    root_cause STRING NOT NULL,
    remediation_steps JSONB NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Distributed Vector Index for sub-second cosine distance searches (<=> operator)
CREATE VECTOR INDEX IF NOT EXISTS idx_incidents_vector 
ON historical_incidents (embedding)
WITH (distance = cosine);

-- -----------------------------------------------------------------------------
-- 2. Active Remediation State Table (Transactional Agent Memory)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS active_remediations (
    remediation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status STRING NOT NULL CHECK (status IN ('PENDING', 'ANALYZING', 'EXECUTING', 'COMPLETED', 'FAILED')),
    current_step INT DEFAULT 1,
    state_payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_remediations_status 
ON active_remediations (status);

-- -----------------------------------------------------------------------------
-- 3. Execution Audit Log (Agent Action Telemetry)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS execution_audit_log (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    remediation_id UUID REFERENCES active_remediations(remediation_id) ON DELETE CASCADE,
    agent_role STRING NOT NULL,
    action_taken STRING NOT NULL,
    ccloud_command_executed STRING,
    status_code INT DEFAULT 200,
    output_summary JSONB,
    executed_at TIMESTAMPTZ DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- 4. Sample Seed Data for Post-Mortem Vector Search Initialization
-- -----------------------------------------------------------------------------
-- Pre-populates historical post-mortems so similarity search returns immediate results.
INSERT INTO historical_incidents (title, service_name, error_signature, root_cause, remediation_steps, embedding)
VALUES (
    'High Memory Utilization - Managed Cluster Node Exhaustion',
    'cockroach-managed-db',
    'OOMKilled: Process killed due to memory limit on node 3',
    'Heavy unindexed vector query scanning caused query heap spike.',
    '{"steps": ["Scale cluster node memory allocation via ccloud CLI", "Apply vector index to target column"]}',
    -- Initial dummy 1536-dim vector representation
    ARRAY_FILL(0.01::FLOAT8, ARRAY[1536])::VECTOR(1536)
) ON CONFLICT DO NOTHING;
