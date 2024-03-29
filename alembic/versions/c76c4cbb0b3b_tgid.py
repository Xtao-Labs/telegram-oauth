"""tgid

Revision ID: c76c4cbb0b3b
Revises: 07a7ace268a7
Create Date: 2024-01-13 16:12:45.884304

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c76c4cbb0b3b'
down_revision = '07a7ace268a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tg_id', sa.BigInteger(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'tg_id')
    # ### end Alembic commands ###
