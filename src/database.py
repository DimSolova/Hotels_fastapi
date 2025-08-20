#src/database
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import setting

engine = create_async_engine(setting.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

class Base(DeclarativeBase):
    pass


