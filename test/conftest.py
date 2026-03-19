import json

import pytest

from src.config import setting
from src.database import Base, engine, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *

from httpx import ASGITransport, AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session",autouse=True)
def check_test_mode():
    assert setting.MODE == "TEST"

@pytest.fixture(scope="function")
async def db():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="session",autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("test/mock_hotels.json", encoding="utf-8") as f:
        hotels_lst = json.load(f)

    with open("test/mock_rooms.json", encoding="utf-8") as f:
        rooms_lst = json.load(f)

    hotels = [HotelAdd(**hotel) for hotel in hotels_lst]
    rooms = [RoomAdd(**room) for room in rooms_lst]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session",autouse=True)
async def register_user(setup_database, ac):

    await ac.post(
        "/auth/register",
        json={
            "email": "test@pes.com",
            "password": "1234"
        }
    )