import falcon
from middleware.body_parser import JSONBodyParser
from middleware.auth import AuthUser
# from middleware.rate_limit import RateLimiter
from utils.database import database_connection


db = database_connection()

middleware = [JSONBodyParser(), AuthUser()]

api = falcon.API(middleware=middleware)


import routes
