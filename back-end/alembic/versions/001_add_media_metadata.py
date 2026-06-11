"""Add franchise, genres and creators to media table.

Revision ID: 001_add_media_metadata
Revises:
Create Date: 2026-06-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "001_add_media_metadata"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if "media" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("media")}

    if "franchise" not in existing:
        op.add_column("media", sa.Column("franchise", sa.String(length=255), nullable=True))
        op.create_index("ix_media_franchise", "media", ["franchise"], unique=False)
    if "genres" not in existing:
        op.add_column("media", sa.Column("genres", sa.JSON(), nullable=True))
    if "creators" not in existing:
        op.add_column("media", sa.Column("creators", sa.JSON(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if "media" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("media")}

    if "franchise" in existing:
        op.drop_index("ix_media_franchise", table_name="media")
        op.drop_column("media", "franchise")
    if "genres" in existing:
        op.drop_column("media", "genres")
    if "creators" in existing:
        op.drop_column("media", "creators")
