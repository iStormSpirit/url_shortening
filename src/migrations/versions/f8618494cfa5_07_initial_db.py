"""07_initial-db

Revision ID: f8618494cfa5
Revises: 6be756d6694c
Create Date: 2022-12-22 23:55:05.558185

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f8618494cfa5'
down_revision = '6be756d6694c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('urls', sa.Column('private', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('urls', 'private')
    # ### end Alembic commands ###
