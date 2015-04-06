import os
import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


TWO_WEEKS = 1209600
SECRET_KEY = os.getenv('SECRET_KEY', None)
assert SECRET_KEY


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def generate_token(user_dict, expiration=TWO_WEEKS):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict)
