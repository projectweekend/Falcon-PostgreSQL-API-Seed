import json
import falcon
from app.utils.auth import hash_password, verify_password
from validation import validate_user_create

USER_FIELDS = ['id', 'email']


class UserResource(object):

    def __init__(self, db):
        self.db = db

    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])

        cursor = self.db.cursor()
        cursor.callproc('sp_app_user_insert', [email, password])

        user_dict = dict(zip(USER_FIELDS, cursor.fetchone()))

        res.body = json.dumps(user_dict)
