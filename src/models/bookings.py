from datetime import date

from sqlalchemy import BigInteger, ForeignKey, Date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rooms.id"))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[int]

    # декоратор как и обычный property, Позволяет использовать функцию как переменную
    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
