"""7

Revision ID: 9cf4b0a64b10
Revises: 457adc3979c8
Create Date: 2022-08-02 09:30:14.455273

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9cf4b0a64b10'
down_revision = '457adc3979c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'cart')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('cart', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
