from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "747662f8a409"
down_revision: Union[str, Sequence[str], None] = "d036fbb08aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("bookings", "total_price")
    op.add_column(
        "bookings",
        sa.Column(
            "total_price",
            sa.Integer(),
            sa.Computed("price * EXTRACT(DAY FROM (date_to - date_from))")
        )
    )

def downgrade() -> None:
    # Удаляем computed колонку
    op.drop_column("bookings", "total_price")
    # Добавляем старую обычную колонку
    op.add_column("bookings", sa.Column("total_price", sa.Integer()))
