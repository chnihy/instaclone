"""empty message

Revision ID: 1cb33a259447
Revises: ffebe75dfb1f
Create Date: 2022-05-31 14:34:38.069465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb33a259447'
down_revision = 'ffebe75dfb1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar_url', sa.String(length=140), nullable=True))
    op.drop_column('user', 'profile_picture_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_picture_url', sa.VARCHAR(length=140), nullable=True))
    op.drop_column('user', 'avatar_url')
    # ### end Alembic commands ###
