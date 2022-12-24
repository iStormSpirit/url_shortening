"""13_initial-db

Revision ID: c1455ae0f3c0
Revises: 7c36a6d9d8dc
Create Date: 2022-12-24 18:08:48.256149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1455ae0f3c0'
down_revision = '7c36a6d9d8dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('urls', sa.Column('author', sa.Integer(), nullable=True))
    op.drop_constraint('urls_user_id_fkey', 'urls', type_='foreignkey')
    op.create_foreign_key(None, 'urls', 'users', ['author'], ['id'], ondelete='CASCADE')
    op.drop_column('urls', 'user_id')
    op.drop_constraint('users_urls_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'urls_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('urls_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_urls_id_fkey', 'users', 'urls', ['urls_id'], ['id'], ondelete='CASCADE')
    op.add_column('urls', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'urls', type_='foreignkey')
    op.create_foreign_key('urls_user_id_fkey', 'urls', 'users', ['user_id'], ['id'])
    op.drop_column('urls', 'author')
    # ### end Alembic commands ###
