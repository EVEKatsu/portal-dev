"""empty message

Revision ID: 73da07cbd495
Revises: 
Create Date: 2019-02-25 13:47:47.347017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73da07cbd495'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tweets',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('screen_name', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('urls', sa.String(), nullable=True),
    sa.Column('ban', sa.Boolean(), nullable=True),
    sa.Column('profile_image_url_https', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweets')
    # ### end Alembic commands ###
