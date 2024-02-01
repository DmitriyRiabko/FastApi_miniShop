"""added unit price column to  order_product_association 

Revision ID: 6a37c15276f3
Revises: ca806aa1c7e2
Create Date: 2024-02-01 11:34:17.980894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a37c15276f3'
down_revision: Union[str, None] = 'ca806aa1c7e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_product_association', sa.Column('unit_price', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_product_association', 'unit_price')
    # ### end Alembic commands ###
