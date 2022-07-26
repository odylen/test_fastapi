"""7

Revision ID: 9186231f0c3d
Revises: e19168690567
Create Date: 2022-08-04 09:43:01.329157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9186231f0c3d'
down_revision = 'e19168690567'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_category_association_category_id_fkey', 'product_category_association', type_='foreignkey')
    op.create_foreign_key(None, 'product_category_association', 'category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_category_association', type_='foreignkey')
    op.create_foreign_key('product_category_association_category_id_fkey', 'product_category_association', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###
