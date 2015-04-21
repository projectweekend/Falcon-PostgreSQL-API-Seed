import redis
from app.config import REDIS_HOST, REDIS_PASSWORD


def redis_connection():
    if REDIS_HOST:
        return redis.StrictRedis(
            host=REDIS_HOST,
            password=REDIS_PASSWORD)
