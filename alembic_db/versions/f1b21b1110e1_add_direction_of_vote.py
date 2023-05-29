"""Add direction of vote

Revision ID: f1b21b1110e1
Revises: bb543961212f
Create Date: 2023-04-30 20:58:17.990016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1b21b1110e1'
down_revision = 'bb543961212f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('direction', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('votes', 'direction')
    # ### end Alembic commands ###