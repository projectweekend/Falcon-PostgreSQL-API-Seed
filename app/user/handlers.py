import json
import falcon
from psycopg2 import IntegrityError
from app import db
from app.utils.auth import hash_password, generate_token
from validation import validate_user_create

USER_FIELDS = ['id', 'email']


class UserResource(object):

    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])

        cursor = db.cursor()

        try:
            cursor.callproc('sp_app_user_insert', [email, password])
        except IntegrityError:
            db.rollback()
            title = 'Conflict'
            description = 'Email in use'
            raise falcon.HTTPConflict(title, description)

        user_dict = dict(zip(USER_FIELDS, cursor.fetchone()))
        db.commit()

        res.body = json.dumps({
            'token': generate_token(user_dict)
        })
