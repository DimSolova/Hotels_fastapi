import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int = 6379):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        """Асинхронное подключение к Redis"""
        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
        )

    async def set(self, key: str, value: str, expire = None) -> None:
        """
        Установить значение в Redis
        :param key: ключ
        :param value: значение
        :param expire: время жизни в секундах
        """
        if not self.redis:
            raise RuntimeError("Redis is not connected")

        await self.redis.set(name=key, value=value, ex=expire)

    async def get(self, key: str):
        """Получить значение по ключу"""
        if not self.redis:
            raise RuntimeError("Redis is not connected")

        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        """Удалить ключ"""
        if not self.redis:
            raise RuntimeError("Redis is not connected")

        return await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()