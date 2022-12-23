"""03_initial-db

Revision ID: 033b9f17f6f7
Revises: ec781b7c28cb
Create Date: 2022-12-22 20:59:30.622023

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '033b9f17f6f7'
down_revision = 'ec781b7c28cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('urls', sa.Column('short_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('urls', 'short_url')
    # ### end Alembic commands ###
