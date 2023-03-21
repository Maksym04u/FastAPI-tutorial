"""add content column to posts table

Revision ID: 0020e1ae898a
Revises: a44312cf48e8
Create Date: 2023-03-14 11:49:40.525528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0020e1ae898a'
down_revision = 'a44312cf48e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
