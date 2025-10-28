from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "579592481a02"
down_revision: Union[str, Sequence[str], None] = "747662f8a409"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем computed колонку, чтобы можно было изменить типы
    op.drop_column("bookings", "total_price")

    # Меняем типы колонок на DATE
    op.alter_column(
        "bookings",
        "date_from",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "date_to",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        existing_nullable=False,
    )
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Date(),
        nullable=False,
    )

    # Добавляем computed колонку заново
    op.add_column(
        "bookings",
        sa.Column(
            "total_price",
            sa.Integer,
            sa.Computed("(price * (date_to - date_from))::int", persisted=True),
            nullable=False,
        ),
    )


def downgrade() -> None:
    # Удаляем computed колонку
    op.drop_column("bookings", "total_price")

    # Возвращаем типы колонок обратно на TIMESTAMP
    op.alter_column("bookings", "date_from", type_=sa.TIMESTAMP(), existing_nullable=False)
    op.alter_column("bookings", "date_to", type_=sa.TIMESTAMP(), existing_nullable=False)
    op.alter_column("bookings", "created_at", type_=sa.TIMESTAMP(), nullable=False)

    # Добавляем computed колонку заново
    op.add_column(
        "bookings",
        sa.Column(
            "total_price",
            sa.Integer,
            sa.Computed("(price * EXTRACT(DAY FROM (date_to - date_from)))::int", persisted=True),
            nullable=False,
        ),
    )
