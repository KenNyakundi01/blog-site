"""empty message

Revision ID: a5e7c6c2b04f
Revises: a93a921d8cee
Create Date: 2020-07-11 10:47:05.562380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5e7c6c2b04f'
down_revision = 'a93a921d8cee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitch', sa.Column('category', sa.Integer(), nullable=True))
    op.drop_constraint('pitch_category_id_fkey', 'pitch', type_='foreignkey')
    op.create_foreign_key(None, 'pitch', 'category', ['category'], ['id'])
    op.drop_column('pitch', 'category_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pitch', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'pitch', type_='foreignkey')
    op.create_foreign_key('pitch_category_id_fkey', 'pitch', 'category', ['category_id'], ['id'])
    op.drop_column('pitch', 'category')
    # ### end Alembic commands ###
