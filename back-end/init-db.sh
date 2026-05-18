#!/bin/bash
# PostgreSQL initialization script
set -e

echo "Creating artiverse database..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Enable UUID extension if needed
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE artiverse TO artiverse_user;
EOSQL

echo "Database initialization complete!"
