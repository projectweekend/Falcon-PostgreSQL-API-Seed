import json
import falcon
from psycopg2 import IntegrityError
from app.utils.auth import hash_password, verify_password, generate_token
from app.utils.hooks import open_cursor_hook, close_cursor_hook
from app.utils.misc import make_code
from validation import validate_user_create, validate_user_auth, validate_request_password_reset

USER_FIELDS = ['id', 'email', 'password', 'is_active', 'is_admin']
USER_TOKEN_FIELDS = ['id', 'email', 'is_active', 'is_admin']


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

        user_dict = dict(zip(USER_TOKEN_FIELDS, self.cursor.fetchone()))

        res.status = falcon.HTTP_201
        res.body = json.dumps({
            'token': generate_token(user_dict)
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

        user_dict = dict(zip(USER_FIELDS, result))

        valid_password = verify_password(password, user_dict.pop('password'))
        if not valid_password:
            raise falcon.HTTPUnauthorized(unauthorized_title, unauthorized_description)

        res.status = falcon.HTTP_200
        res.body = json.dumps({
            'token': generate_token(user_dict)
        })


@falcon.before(open_cursor_hook)
@falcon.after(close_cursor_hook)
class PasswordResetRequestResource(object):

    @falcon.before(validate_request_password_reset)
    def on_post(self, req, res):
        email = req.context['data']['email']

        self.cursor.callproc('sp_lookup_user_by_email', [email, ])
        result = self.cursor.fetchone()
        if result:
            user_dict = dict(zip(USER_FIELDS, result))
            self.cursor.callproc('sp_app_password_reset_insert', [user_dict['id'], make_code(), ])
            # TODO: send email using preferred method

        res.status = falcon.HTTP_201
        res.body = json.dumps({})
