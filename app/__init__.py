import falcon
from middleware import JSONBodyParser
from utils.database import database_connection


middleware = [JSONBodyParser()]

api = falcon.API(middleware=middleware)
db = database_connection()


import routes
