"""add last few columns to posts table

Revision ID: ac14afdb693c
Revises: 9502188f1faf
Create Date: 2023-03-19 21:01:21.247591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac14afdb693c'
down_revision = '9502188f1faf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="True", nullable=False))

    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                                     nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
