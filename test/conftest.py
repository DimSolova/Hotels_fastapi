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