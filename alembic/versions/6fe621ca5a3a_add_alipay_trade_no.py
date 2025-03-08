"""add alipay_trade_no

Revision ID: 6fe621ca5a3a
Revises: 6ac5c0df6181
Create Date: 2024-09-04 14:36:33.127853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fe621ca5a3a'
down_revision: Union[str, None] = '6ac5c0df6181'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('alipay_trade_no', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'alipay_trade_no')
    # ### end Alembic commands ###
