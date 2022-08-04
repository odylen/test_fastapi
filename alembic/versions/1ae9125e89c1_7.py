"""7

Revision ID: 1ae9125e89c1
Revises: 7eadc50ec158
Create Date: 2022-08-04 14:35:32.982732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ae9125e89c1'
down_revision = '7eadc50ec158'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bakery', 'is_active')
    op.drop_column('bakery', 'sort')
    op.add_column('delivery_order', sa.Column('bakery_id', sa.Integer(), nullable=True))
    op.drop_constraint('delivery_order_shop_id_fkey', 'delivery_order', type_='foreignkey')
    op.create_foreign_key(None, 'delivery_order', 'bakery', ['bakery_id'], ['id'])
    op.drop_column('delivery_order', 'shop_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('delivery_order', sa.Column('shop_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'delivery_order', type_='foreignkey')
    op.create_foreign_key('delivery_order_shop_id_fkey', 'delivery_order', 'bakery', ['shop_id'], ['id'])
    op.drop_column('delivery_order', 'bakery_id')
    op.add_column('bakery', sa.Column('sort', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('bakery', sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###