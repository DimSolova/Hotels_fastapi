"""initial migration

Revision ID: ba9709399b3a
Revises:
Create Date: 2025-08-20 20:58:19.681588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'ba9709399b3a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('hotels')
