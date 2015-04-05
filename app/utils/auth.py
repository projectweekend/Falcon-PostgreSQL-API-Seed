import os
import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


TWO_WEEKS = 1209600
SECRET_KEY = os.getenv('SECRET_KEY', None)
assert SECRET_KEY


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed


def generate_token(user_dict, expiration=TWO_WEEKS):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict)


def verify_token(token):
    s = Serializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return None
    return data
