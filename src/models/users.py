from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    hashed_password:Mapped[str] = mapped_column(String(200))
    nickname: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column(Integer)