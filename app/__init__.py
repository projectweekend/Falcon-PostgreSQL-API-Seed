import falcon
from middleware.body_parser import JSONBodyParser
from utils.database import database_connection


db = database_connection()

middleware = [JSONBodyParser()]

api = falcon.API(middleware=middleware)


import routes
