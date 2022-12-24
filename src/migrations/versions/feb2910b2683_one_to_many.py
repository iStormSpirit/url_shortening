"""one-to-many

Revision ID: feb2910b2683
Revises: a545cd8de433
Create Date: 2022-12-24 19:57:21.185410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feb2910b2683'
down_revision = 'a545cd8de433'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('urls', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'urls', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'urls', type_='foreignkey')
    op.drop_column('urls', 'author_id')
    # ### end Alembic commands ###