"""Add new field

Revision ID: bc3a1cc414d6
Revises: 01a5743a7a59
Create Date: 2021-04-12 10:43:31.981873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3a1cc414d6'
down_revision = '01a5743a7a59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('reply_status', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'reply_status')
    # ### end Alembic commands ###
