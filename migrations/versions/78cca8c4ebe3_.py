"""empty message

Revision ID: 78cca8c4ebe3
Revises: 95e35b72e26a
Create Date: 2020-05-08 21:45:41.065044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78cca8c4ebe3'
down_revision = '95e35b72e26a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Artist')
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.create_table('Artist',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Artist_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Artist_pkey')
    )
    # ### end Alembic commands ###
