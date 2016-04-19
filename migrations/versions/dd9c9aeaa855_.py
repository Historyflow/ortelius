"""empty message

Revision ID: dd9c9aeaa855
Revises: 75cc11349479
Create Date: 2016-04-18 23:39:59.992294

"""

# revision identifiers, used by Alembic.
revision = 'dd9c9aeaa855'
down_revision = '75cc11349479'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shape', sa.Column('fact_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shape', 'fact', ['fact_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shape', type_='foreignkey')
    op.drop_column('shape', 'fact_id')
    ### end Alembic commands ###