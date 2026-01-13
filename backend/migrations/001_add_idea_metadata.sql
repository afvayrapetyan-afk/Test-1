-- Migration: Add metadata and financial fields to ideas table
-- Date: 2026-01-14
-- Description: Add category, emoji, source, financial projections, and trending flag
-- SQLite compatible version

-- Add new columns (SQLite doesn't support IF NOT EXISTS in ALTER TABLE ADD COLUMN)
ALTER TABLE ideas ADD COLUMN emoji VARCHAR(10) DEFAULT '💡';
ALTER TABLE ideas ADD COLUMN source VARCHAR(200) DEFAULT 'AI Analysis';
ALTER TABLE ideas ADD COLUMN category VARCHAR(50);
ALTER TABLE ideas ADD COLUMN is_trending INTEGER DEFAULT 0;

-- Add financial projection columns
ALTER TABLE ideas ADD COLUMN investment INTEGER;
ALTER TABLE ideas ADD COLUMN payback_months INTEGER;
ALTER TABLE ideas ADD COLUMN margin INTEGER;
ALTER TABLE ideas ADD COLUMN arr INTEGER;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_ideas_category ON ideas(category);
CREATE INDEX IF NOT EXISTS idx_ideas_trending ON ideas(is_trending);

-- Update existing records with default values
UPDATE ideas
SET emoji = '💡',
    source = 'AI Analysis',
    category = 'ai',
    is_trending = 0,
    investment = 50000,
    payback_months = 12,
    margin = 30,
    arr = 100000;
