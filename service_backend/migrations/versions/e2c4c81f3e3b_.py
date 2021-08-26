"""empty message

Revision ID: e2c4c81f3e3b
Revises: 3b7a95bb6d22
Create Date: 2021-08-26 11:07:23.867551

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e2c4c81f3e3b'
down_revision = '3b7a95bb6d22'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('benchmark', 'created_at',  new_column_name='upload_datetime')
    op.alter_column('flavor', 'created_at',  new_column_name='upload_datetime')
    op.alter_column('report', 'created_at',  new_column_name='upload_datetime')
    op.alter_column('result', 'created_at',  new_column_name='upload_datetime')
    op.alter_column('result', 'executed_at',  new_column_name='execution_datetime')
    op.alter_column('site', 'created_at',  new_column_name='upload_datetime')
    op.alter_column('user', 'created_at',  new_column_name='upload_datetime')
    # ### end Alembic commands ###


def downgrade():
    op.alter_column('benchmark', 'upload_datetime',  new_column_name='created_at')
    op.alter_column('flavor', 'upload_datetime',  new_column_name='created_at')
    op.alter_column('report', 'upload_datetime',  new_column_name='created_at')
    op.alter_column('result', 'upload_datetime',  new_column_name='created_at')
    op.alter_column('result', 'execution_datetime',  new_column_name='executed_at')
    op.alter_column('site', 'upload_datetime',  new_column_name='created_at')
    op.alter_column('user', 'upload_datetime',  new_column_name='created_at')
    # ### end Alembic commands ###
