import pytest

from src.config import setting
from src.database import Base, engine, engine_null_pool
from src.models import *

@pytest.fixture(scope="session",autouse=True)
async def async_main() -> None:
    print("Я Фикстура")
    assert setting.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)