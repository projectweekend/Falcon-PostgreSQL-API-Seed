from app.utils.auth import verify_token


class AuthUser(object):

    def process_request(self, req, res):
        if req.auth:
            req.context['auth_user'] = verify_token(req.auth)
