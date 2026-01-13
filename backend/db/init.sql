-- ============================================================================
-- AI Business Portfolio Manager - Database Schema
-- ============================================================================
-- Version: 1.0
-- Created: 2026-01-13
-- Description: Initial database schema for trends, ideas, businesses, and agents
-- ============================================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- ============================================================================
-- Table: trends
-- ============================================================================

CREATE TABLE IF NOT EXISTS trends (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url TEXT,
    source VARCHAR(50) NOT NULL,  -- reddit, google_trends, telegram, vk, youtube, instagram
    category VARCHAR(50),
    tags TEXT[],

    -- Metrics
    engagement_score INTEGER DEFAULT 0,
    velocity FLOAT DEFAULT 0,  -- Trend velocity (growth rate)

    -- Metadata
    discovered_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',

    -- Constraints
    CONSTRAINT valid_source CHECK (source IN ('reddit', 'google_trends', 'telegram', 'vk', 'youtube', 'instagram', 'facebook', 'product_hunt')),
    CONSTRAINT valid_engagement CHECK (engagement_score >= 0)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_trends_source ON trends(source);
CREATE INDEX IF NOT EXISTS idx_trends_category ON trends(category);
CREATE INDEX IF NOT EXISTS idx_trends_engagement ON trends(engagement_score DESC);
CREATE INDEX IF NOT EXISTS idx_trends_discovered ON trends(discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_trends_tags ON trends USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_trends_metadata ON trends USING GIN(metadata);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_trends_search ON trends USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')));

-- Comments
COMMENT ON TABLE trends IS 'Discovered trends from various data sources';
COMMENT ON COLUMN trends.velocity IS 'Growth rate of the trend (engagement per day)';
COMMENT ON COLUMN trends.metadata IS 'Flexible JSON field for source-specific data';

-- ============================================================================
-- Table: ideas
-- ============================================================================

CREATE TABLE IF NOT EXISTS ideas (
    id SERIAL PRIMARY KEY,
    trend_id INTEGER REFERENCES trends(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,

    -- Scores (0-100 for each metric)
    market_size_score INTEGER CHECK (market_size_score BETWEEN 0 AND 100),
    competition_score INTEGER CHECK (competition_score BETWEEN 0 AND 100),
    demand_score INTEGER CHECK (demand_score BETWEEN 0 AND 100),
    monetization_score INTEGER CHECK (monetization_score BETWEEN 0 AND 100),
    feasibility_score INTEGER CHECK (feasibility_score BETWEEN 0 AND 100),
    time_to_market_score INTEGER CHECK (time_to_market_score BETWEEN 0 AND 100),

    -- Calculated overall score (average of 6 metrics)
    total_score INTEGER GENERATED ALWAYS AS (
        COALESCE(
            (COALESCE(market_size_score, 0) +
             COALESCE(competition_score, 0) +
             COALESCE(demand_score, 0) +
             COALESCE(monetization_score, 0) +
             COALESCE(feasibility_score, 0) +
             COALESCE(time_to_market_score, 0)) / 6,
            0
        )
    ) STORED,

    -- Analysis details
    analysis JSONB DEFAULT '{}',  -- Full LLM analysis with reasoning
    analyzed_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Status workflow
    status VARCHAR(20) DEFAULT 'pending',  -- pending, approved, rejected, in_development

    CONSTRAINT valid_status CHECK (status IN ('pending', 'approved', 'rejected', 'in_development', 'launched'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_ideas_total_score ON ideas(total_score DESC);
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
CREATE INDEX IF NOT EXISTS idx_ideas_trend ON ideas(trend_id);
CREATE INDEX IF NOT EXISTS idx_ideas_analyzed ON ideas(analyzed_at DESC);

-- Comments
COMMENT ON TABLE ideas IS 'Business ideas generated from analyzed trends';
COMMENT ON COLUMN ideas.total_score IS 'Automatically calculated average of all 6 scores';
COMMENT ON COLUMN ideas.analysis IS 'Complete LLM analysis including reasoning for each score';

-- ============================================================================
-- Table: businesses
-- ============================================================================

CREATE TABLE IF NOT EXISTS businesses (
    id SERIAL PRIMARY KEY,
    idea_id INTEGER REFERENCES ideas(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    domain VARCHAR(100) UNIQUE,
    description TEXT,

    -- Status
    status VARCHAR(50) DEFAULT 'development',  -- development, launched, active, paused, closed

    -- Business Metrics
    revenue_monthly DECIMAL(10, 2) DEFAULT 0,
    users_count INTEGER DEFAULT 0,
    mrr DECIMAL(10, 2) DEFAULT 0,  -- Monthly Recurring Revenue

    -- Lifecycle Timestamps
    developed_at TIMESTAMP,
    launched_at TIMESTAMP,
    paused_at TIMESTAMP,
    closed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- Additional data
    metadata JSONB DEFAULT '{}',

    CONSTRAINT valid_business_status CHECK (status IN ('development', 'launched', 'active', 'paused', 'closed'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_businesses_status ON businesses(status);
CREATE INDEX IF NOT EXISTS idx_businesses_domain ON businesses(domain);
CREATE INDEX IF NOT EXISTS idx_businesses_revenue ON businesses(revenue_monthly DESC);
CREATE INDEX IF NOT EXISTS idx_businesses_launched ON businesses(launched_at DESC);

-- Comments
COMMENT ON TABLE businesses IS 'Active businesses managed by the system';
COMMENT ON COLUMN businesses.mrr IS 'Monthly Recurring Revenue';

-- ============================================================================
-- Table: agent_executions
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_executions (
    id SERIAL PRIMARY KEY,
    agent_type VARCHAR(50) NOT NULL,  -- trend_scout, idea_analyst, dev_agent, marketing_agent, sales_agent

    -- Execution details
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',

    -- Status tracking
    status VARCHAR(20) DEFAULT 'pending',  -- pending, running, completed, failed
    error TEXT,

    -- Timing
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Cost tracking
    llm_tokens_used INTEGER DEFAULT 0,
    llm_cost_usd DECIMAL(10, 4) DEFAULT 0,

    -- Metadata
    metadata JSONB DEFAULT '{}',

    CONSTRAINT valid_agent_status CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_executions_agent ON agent_executions(agent_type);
CREATE INDEX IF NOT EXISTS idx_executions_status ON agent_executions(status);
CREATE INDEX IF NOT EXISTS idx_executions_started ON agent_executions(started_at DESC);

-- Comments
COMMENT ON TABLE agent_executions IS 'Log of all AI agent executions for monitoring and analytics';
COMMENT ON COLUMN agent_executions.llm_cost_usd IS 'Estimated cost of LLM API calls for this execution';

-- ============================================================================
-- Table: users (Optional - for multi-user support)
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,

    -- Profile
    full_name VARCHAR(200),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ============================================================================
-- Views for Analytics
-- ============================================================================

-- Top performing ideas
CREATE OR REPLACE VIEW top_ideas AS
SELECT
    i.id,
    i.title,
    i.total_score,
    i.status,
    t.title as trend_title,
    t.source,
    i.analyzed_at
FROM ideas i
LEFT JOIN trends t ON i.trend_id = t.id
WHERE i.total_score > 70
ORDER BY i.total_score DESC
LIMIT 100;

-- Recent trends by source
CREATE OR REPLACE VIEW recent_trends_by_source AS
SELECT
    source,
    COUNT(*) as count,
    AVG(engagement_score) as avg_engagement,
    MAX(discovered_at) as latest_trend
FROM trends
WHERE discovered_at > NOW() - INTERVAL '7 days'
GROUP BY source
ORDER BY count DESC;

-- Business performance overview
CREATE OR REPLACE VIEW business_performance AS
SELECT
    status,
    COUNT(*) as count,
    SUM(revenue_monthly) as total_revenue,
    AVG(revenue_monthly) as avg_revenue,
    SUM(users_count) as total_users
FROM businesses
GROUP BY status
ORDER BY
    CASE status
        WHEN 'active' THEN 1
        WHEN 'launched' THEN 2
        WHEN 'development' THEN 3
        WHEN 'paused' THEN 4
        WHEN 'closed' THEN 5
    END;

-- Agent execution stats
CREATE OR REPLACE VIEW agent_stats AS
SELECT
    agent_type,
    status,
    COUNT(*) as execution_count,
    AVG(duration_seconds) as avg_duration_seconds,
    SUM(llm_cost_usd) as total_cost_usd,
    MAX(started_at) as last_execution
FROM agent_executions
WHERE started_at > NOW() - INTERVAL '30 days'
GROUP BY agent_type, status
ORDER BY agent_type, status;

-- ============================================================================
-- Functions & Triggers
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for auto-updating updated_at
CREATE TRIGGER update_ideas_updated_at BEFORE UPDATE ON ideas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_businesses_updated_at BEFORE UPDATE ON businesses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate agent execution duration
CREATE OR REPLACE FUNCTION calculate_execution_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.completed_at IS NOT NULL AND NEW.started_at IS NOT NULL THEN
        NEW.duration_seconds = EXTRACT(EPOCH FROM (NEW.completed_at - NEW.started_at))::INTEGER;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_agent_duration BEFORE UPDATE ON agent_executions
    FOR EACH ROW EXECUTE FUNCTION calculate_execution_duration();

-- ============================================================================
-- Initial Data (Optional)
-- ============================================================================

-- Insert sample trend categories
DO $$
BEGIN
    -- Categories will be populated dynamically, but we can insert some examples
    INSERT INTO trends (title, description, source, category, engagement_score, tags)
    VALUES
        ('AI-powered note-taking app', 'Automatic meeting transcription and summarization', 'reddit', 'productivity', 1523, ARRAY['AI', 'SaaS', 'productivity']),
        ('No-code website builder for restaurants', 'Drag-and-drop website builder specifically for restaurants', 'product_hunt', 'saas', 892, ARRAY['no-code', 'restaurants', 'websites'])
    ON CONFLICT DO NOTHING;
END $$;

-- ============================================================================
-- Grants (for application user)
-- ============================================================================

-- Grant permissions to application user
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_user') THEN
        GRANT USAGE ON SCHEMA public TO app_user;
        GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
        GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

        -- Grant select on views
        GRANT SELECT ON top_ideas TO app_user;
        GRANT SELECT ON recent_trends_by_source TO app_user;
        GRANT SELECT ON business_performance TO app_user;
        GRANT SELECT ON agent_stats TO app_user;
    END IF;
END $$;

-- ============================================================================
-- Statistics & Optimization
-- ============================================================================

-- Analyze tables for better query planning
ANALYZE trends;
ANALYZE ideas;
ANALYZE businesses;
ANALYZE agent_executions;

-- ============================================================================
-- Completion
-- ============================================================================

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'Database schema initialized successfully!';
    RAISE NOTICE 'Tables created: trends, ideas, businesses, agent_executions, users';
    RAISE NOTICE 'Views created: top_ideas, recent_trends_by_source, business_performance, agent_stats';
    RAISE NOTICE 'Ready for application startup.';
END $$;
