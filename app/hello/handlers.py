import json


class HelloResource(object):

    def on_get(self, req, resp):
        resp.body = json.dumps({
            "msg": "Hello!",
        })
