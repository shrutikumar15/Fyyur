"""empty message

Revision ID: 41d9b40dea96
Revises: 6ef244f6a22a
Create Date: 2020-05-12 03:55:53.952801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41d9b40dea96'
down_revision = '6ef244f6a22a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('venues', sa.ARRAY(sa.String()), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Area')
    # ### end Alembic commands ###
