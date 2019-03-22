import hashlib, binascii
# to be replaced by python 3.6 secrets module
from app.utils import secrets
from app.utils import jwt


def get_password_hash(password, salt):
    dk = hashlib.pbkdf2_hmac('md5', password.encode('utf-8'), salt, 100000)
    return binascii.hexlify(dk)


def get_salt(n=16):
    return secrets.token_bytes(n)


def get_jwt(user):
    header = {
        "typ": "JWT",
        "alg": "HS256"
    }
    payload = {
        "iat": 1422779638,
        "exp": 1623780638,
        "userId": str(user['_id']),
        "name": "%s %s"%(user['first_name'], user['last_name'])
    }
    return jwt.sign(header, payload,secrets.get_jwt_secret())
