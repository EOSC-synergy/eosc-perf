"""empty message

Revision ID: 1208d5f696a6
Revises: e2c4c81f3e3b
Create Date: 2021-08-26 11:14:42.828414

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '1208d5f696a6'
down_revision = 'e2c4c81f3e3b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'user', ['sub', 'iss'])
    # ### end Alembic commands ###


def downgrade():
    op.drop_constraint(None, 'user', type_='unique')
    # ### end Alembic commands ###
