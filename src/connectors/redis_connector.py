import redis.asyncio as redis
import logging

class RedisManager:
    _redis: redis.Redis
    def __init__(self, host: str, port: int = 6379):
        self.host = host
        self.port = port

    async def connect(self) -> None:
        """Асинхронное подключение к Redis"""
        logging.info(f"Начинаю подключение к Redis {self.host}, port={self.port}")
        self._redis = redis.Redis(
            host=self.host,
            port=self.port,
        )
        logging.info(f"Успешно подключены к Redis {self.host}, port={self.port}")

    async def set(self, key: str, value: str, expire= int | None) -> None:
        """
        Установить значение в Redis
        :param key: ключ
        :param value: значение
        :param expire: время жизни в секундах
        """
        if not self._redis:
            raise RuntimeError("Redis is not connected")

        await self._redis.set(name=key, value=value, ex=expire)

    async def get(self, key: str):
        """Получить значение по ключу"""
        if not self._redis:
            raise RuntimeError("Redis is not connected")

        return await self._redis.get(key)

    async def delete(self, key: str) -> int:
        """Удалить ключ"""
        if not self._redis:
            raise RuntimeError("Redis is not connected")

        return await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
