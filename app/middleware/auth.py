from app.utils.auth import verify_token


class AuthUser(object):

    def process_request(self, req, res):
        req.context['auth_user'] = verify_token(req.auth) if req.auth else None
