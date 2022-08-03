"""7

Revision ID: 57fc5d717e75
Revises: 5357938ca505
Create Date: 2022-08-02 11:27:51.405029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57fc5d717e75'
down_revision = '5357938ca505'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_delivery_address_id'), 'delivery_address', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_delivery_address_id'), table_name='delivery_address')
    op.drop_table('delivery_address')
    # ### end Alembic commands ###
