"""add foreign key to posts table

Revision ID: 9502188f1faf
Revises: 7813aebbe345
Create Date: 2023-03-19 20:41:55.298662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9502188f1faf'
down_revision = '7813aebbe345'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                                     nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
    pass
