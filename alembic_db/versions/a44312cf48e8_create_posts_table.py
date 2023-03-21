"""create posts table

Revision ID: a44312cf48e8
Revises: 
Create Date: 2023-03-14 11:18:27.957872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a44312cf48e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False)  # We use sa.* to not import anything from sqlalchemy
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
