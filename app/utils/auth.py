import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password, hashed) == hashed
