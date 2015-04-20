import os


TWO_WEEKS = 1209600

SECRET_KEY = os.getenv('SECRET_KEY', None)
assert SECRET_KEY

TOKEN_EXPIRES = TWO_WEEKS

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgres://postgres@{0}:5432/postgres'.format(os.getenv('DB_PORT_5432_TCP_ADDR', None)))
assert DATABASE_URL

REDIS_HOST = os.getenv('REDIS_HOST', None)
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
