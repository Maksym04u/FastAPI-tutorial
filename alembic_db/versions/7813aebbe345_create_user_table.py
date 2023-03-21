"""Create user table

Revision ID: 7813aebbe345
Revises: 0020e1ae898a
Create Date: 2023-03-14 12:03:47.417918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7813aebbe345'
down_revision = '0020e1ae898a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),

    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
