import redis
from app.config import REDIS_HOST, REDIS_PASSWORD


def redis_connection():
    if REDIS_HOST and REDIS_PASSWORD:
        return redis.StrictRedis(
            host=REDIS_HOST,
            db='rate_limit',
            password=REDIS_PASSWORD)
