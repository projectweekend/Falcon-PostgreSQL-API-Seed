from app import api, db
from hello import handlers as hello_handlers
from user import handlers as user_handlers


api.add_route("/", hello_handlers.HelloResource())
api.add_route('/user', user_handlers.UserResource(db))
