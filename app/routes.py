from app import api
from user import handlers as user_handlers


api.add_route('/user', user_handlers.UserResource())
