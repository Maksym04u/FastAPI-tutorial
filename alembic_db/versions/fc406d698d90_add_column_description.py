"""Add column description

Revision ID: fc406d698d90
Revises: e4ffff19894e
Create Date: 2023-04-27 14:38:25.065469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc406d698d90'
down_revision = 'e4ffff19894e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('description', sa.String(length=50), server_default="Some content"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'description')
    # ### end Alembic commands ###
