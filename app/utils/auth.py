import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSigSerializer
from app.config import SECRET_KEY, TOKEN_EXPIRES


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed


def generate_token(user_dict, expiration=TOKEN_EXPIRES):
    s = TimedSigSerializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict)
