from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d036fbb08aac"
down_revision: Union[str, Sequence[str], None] = "d54183e4aa78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("total_price", sa.Integer(), nullable=True))
    op.add_column("bookings", sa.Column("created_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("bookings", "created_at")
    op.drop_column("bookings", "total_price")
