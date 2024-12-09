"""Добавлено поле created_at в таблицу hotels

Revision ID: 9dda9b94d96a
Revises: 57ad08dfc090
Create Date: 2024-11-13 13:07:41.365987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dda9b94d96a'
down_revision: Union[str, None] = '57ad08dfc090'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('created_at', sa.Date(), nullable=False))
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('hotels', 'created_at')
    # ### end Alembic commands ###
