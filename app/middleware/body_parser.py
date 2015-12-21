import json
import falcon


class JSONBodyParser(object):

    def process_request(self, req, res):
        if req.content_type == 'application/json':
            body = req.stream.read().decode('utf-8')
            try:
                req.context['data'] = json.loads(body)
            except ValueError:
                message = "Request body is not valid 'application/json'"
                raise falcon.HTTPBadRequest('Bad request', message)
