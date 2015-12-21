import json
import falcon
from psycopg2 import IntegrityError
from app.utils.auth import hash_password, verify_password, generate_token
from app.utils.hooks import open_cursor_hook, close_cursor_hook, auth_required
from app.utils.misc import make_code
from app.user.validation import (
    validate_user_create, validate_user_auth, validate_request_password_reset,
    validate_confirm_password_reset)


@falcon.before(open_cursor_hook)
@falcon.after(close_cursor_hook)
class UserResource(object):

    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])

        try:
            self.cursor.callproc('sp_user_insert', [email, password])
        except IntegrityError:
            title = 'Conflict'
            description = 'Email in use'
            raise falcon.HTTPConflict(title, description)

        result = self.cursor.fetchone()[0]

        res.status = falcon.HTTP_201
        res.body = json.dumps({
            'token': generate_token(result)
        })


@falcon.before(open_cursor_hook)
@falcon.after(close_cursor_hook)
class AuthenticationResource(object):

    @falcon.before(validate_user_auth)
    def on_post(self, req, res):
        unauthorized_title = 'Unauthorized'
        unauthorized_description = 'Invalid credentials'

        email = req.context['data']['email']
        password = req.context['data']['password']

        self.cursor.callproc('sp_lookup_user_by_email', [email, ])

        result = self.cursor.fetchone()
        if result is None:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        result = result[0]

        valid_password = verify_password(password, result.pop('password'))
        if not valid_password:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        res.status = falcon.HTTP_200
        res.body = json.dumps({
            'token': generate_token(result)
        })


@falcon.before(open_cursor_hook)
@falcon.after(close_cursor_hook)
class PasswordResetRequestResource(object):

    @falcon.before(validate_request_password_reset)
    def on_post(self, req, res):
        email = req.context['data']['email']
        self.cursor.callproc('sp_reset_password_request', [email, make_code(), ])
        res.status = falcon.HTTP_201
        res.body = json.dumps({})


@falcon.before(open_cursor_hook)
@falcon.after(close_cursor_hook)
class PasswordResetConfirmResource(object):

    @falcon.before(validate_confirm_password_reset)
    def on_post(self, req, res):
        code = req.context['data']['code']
        password = hash_password(req.context['data']['password'])
        self.cursor.callproc('sp_reset_password', [code, password, ])
        result = self.cursor.fetchone()
        res.status = falcon.HTTP_200 if result[0] else falcon.HTTP_401
        res.body = json.dumps({})


# Handlers for test routes
class AuthTestResource(object):

    @falcon.before(auth_required)
    def on_get(self, req, res):
        res.status = falcon.HTTP_200
        res.body = json.dumps({
            'email': req.context['auth_user']['email']
        })
