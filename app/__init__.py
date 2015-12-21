import falcon
from app.middleware.body_parser import JSONBodyParser
from app.middleware.auth import AuthUser
from app.utils.database import database_connection


db = database_connection()

middleware = [JSONBodyParser(), AuthUser()]

api = falcon.API(middleware=middleware)


from app import routes
