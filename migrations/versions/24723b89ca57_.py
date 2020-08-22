"""empty message

Revision ID: 24723b89ca57
Revises: 9ae366a10c03
Create Date: 2018-05-01 18:24:04.179763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24723b89ca57'
down_revision = '9ae366a10c03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('roomno', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room')
    # ### end Alembic commands ###
