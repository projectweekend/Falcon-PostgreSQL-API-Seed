from app import api
from hello import handlers as hello_handlers


api.add_route("/", hello_handlers.HelloResource())
