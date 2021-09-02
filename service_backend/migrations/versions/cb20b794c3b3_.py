"""empty message

Revision ID: cb20b794c3b3
Revises: 1208d5f696a6
Create Date: 2021-09-02 08:22:16.022411

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cb20b794c3b3'
down_revision = '1208d5f696a6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('result', '_benchmark_id', new_column_name='benchmark_id')
    op.alter_column('result', '_site_id', new_column_name='site_id')
    op.alter_column('result', '_flavor_id', new_column_name='flavor_id')
    # ### end Alembic commands ###


def downgrade():
    op.alter_column('result', 'benchmark_id', new_column_name='_benchmark_id')
    op.alter_column('result', 'site_id', new_column_name='_site_id')
    op.alter_column('result', 'flavor_id', new_column_name='_flavor_id')
    # ### end Alembic commands ###
