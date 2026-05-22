#!/bin/bash
# Database schema update script to fix missing columns

echo "Updating database schema..."

# Add missing columns to users table
docker exec artiverse-postgres psql -U artiverse_user -d artiverse << 'EOF'
-- Add missing columns if they don't exist
ALTER TABLE users ADD COLUMN IF NOT EXISTS streak_days INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_date TIMESTAMP WITH TIME ZONE;

-- Verify the schema
\d users
EOF

echo "Database schema update complete!"