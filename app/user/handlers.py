import json
import falcon
from app.utils.auth import hash_password, verify_password
from validation import validate_user_create


class UserResource(object):

    def __init__(self, db):
        self.db = db

    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        email = req.context['data']['email']
        password = hash_password(req.context['data']['password'])
        res.body = json.dumps({})
