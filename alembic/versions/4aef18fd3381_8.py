"""8

Revision ID: 4aef18fd3381
Revises: 3fb04e4ced35
Create Date: 2022-08-05 07:56:51.612509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aef18fd3381'
down_revision = '3fb04e4ced35'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('favorite_product_association_product_id_fkey', 'favorite_product_association', type_='foreignkey')
    op.drop_constraint('favorite_product_association_user_id_fkey', 'favorite_product_association', type_='foreignkey')
    op.create_foreign_key(None, 'favorite_product_association', 'product', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'favorite_product_association', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'favorite_product_association', type_='foreignkey')
    op.drop_constraint(None, 'favorite_product_association', type_='foreignkey')
    op.create_foreign_key('favorite_product_association_user_id_fkey', 'favorite_product_association', 'user', ['user_id'], ['id'])
    op.create_foreign_key('favorite_product_association_product_id_fkey', 'favorite_product_association', 'product', ['product_id'], ['id'])
    # ### end Alembic commands ###
