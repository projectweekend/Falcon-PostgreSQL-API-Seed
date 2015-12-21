import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSigSerializer
from itsdangerous import SignatureExpired, BadSignature
from app.config import SECRET_KEY, TOKEN_EXPIRES


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed.encode('utf-8')).decode('utf-8') == hashed


def generate_token(user_dict, expiration=TOKEN_EXPIRES):
    s = TimedSigSerializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict).decode('utf-8')


def verify_token(token):
    s = TimedSigSerializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return None
    return data
