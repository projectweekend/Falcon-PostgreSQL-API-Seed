import psycopg2
from urlparse import urlparse
from app.config import DATABASE_URL


def database_connection():
    parsed = urlparse(DATABASE_URL)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    database = parsed.path.strip('/')

    connection = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
    connection.set_session(autocommit=True)

    return connection
