from src.connectors.redis_connector import RedisManager
from src.config import setting

redis_managet = RedisManager(
    host=setting.REDIS_HOST,
    port=setting.REDIS_PORT
)