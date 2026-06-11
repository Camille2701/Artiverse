"""Lightweight schema patches for existing databases.

SQLAlchemy create_all() does not ALTER existing tables. When new columns are
added to models, this module applies the missing columns on startup so dev
environments with persisted Postgres volumes keep working without a full reset.
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection


async def ensure_schema_updates(conn: AsyncConnection) -> None:
    """Add columns introduced after the initial schema was deployed."""
    await conn.execute(text("""
        ALTER TABLE media
        ADD COLUMN IF NOT EXISTS franchise VARCHAR(255)
    """))
    await conn.execute(text("""
        ALTER TABLE media
        ADD COLUMN IF NOT EXISTS genres JSON
    """))
    await conn.execute(text("""
        ALTER TABLE media
        ADD COLUMN IF NOT EXISTS creators JSON
    """))
    await conn.execute(text("""
        CREATE INDEX IF NOT EXISTS ix_media_franchise ON media (franchise)
    """))
