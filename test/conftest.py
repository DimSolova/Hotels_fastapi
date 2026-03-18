import json

import pytest

from src.config import setting
from src.database import Base, engine, engine_null_pool
from src.main import app
from src.models import *

from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session",autouse=True)
def check_test_mode():
    assert setting.MODE == "TEST"

@pytest.fixture(scope="session",autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Отели
        with open("test/mock_hotels.json", encoding="utf-8") as f:
            hotels = json.load(f)
        for hotel in hotels:
            await ac.post("/hotels", json=hotel)

        # Комнаты
        with open("test/mock_rooms.json", encoding="utf-8") as f:
            rooms = json.load(f)

        for room in rooms:
            hotel_id = room.pop("hotel_id")  # убираем, если есть
            url = f"/hotels/{hotel_id}/rooms"
            await ac.post(
                url,  # ← вот здесь главное
                json=room
            )


@pytest.fixture(scope="session",autouse=True)
async def register_user(setup_database):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={
                "email": "test@pes.com",
                "password": "1234"
            }
        )
        assert response.status_code in (200, 201), f"Регистрация не удалась: {response.text}"