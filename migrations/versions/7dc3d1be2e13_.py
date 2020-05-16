"""empty message

Revision ID: 7dc3d1be2e13
Revises: f880f755dc9a
Create Date: 2020-05-14 22:14:02.311033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dc3d1be2e13'
down_revision = 'f880f755dc9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Area', sa.Column('ids', sa.ARRAY(sa.Integer()), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Area', 'ids')
    # ### end Alembic commands ###