from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "27417c0315f2"
down_revision: Union[str, Sequence[str], None] = "91ad49a511de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "nickname")
    op.drop_column("users", "age")


def downgrade() -> None:
    op.add_column("users", sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column(
        "users",
        sa.Column("nickname", sa.VARCHAR(length=25), autoincrement=False, nullable=False),
    )
