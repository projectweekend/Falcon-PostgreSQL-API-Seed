import os
import psycopg2
from urlparse import urlparse


def database_connection():
    docker_db_host = os.getenv('DB_PORT_5432_TCP_ADDR', None)
    if docker_db_host:
        database_url = 'postgres://postgres:123456@{0}:5432/postgres'.format(docker_db_host)
    else:
        database_url = os.getenv('DATABASE_URL', None)

    assert database_url

    parsed = urlparse(database_url)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    database = parsed.path.strip('/')

    return psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
