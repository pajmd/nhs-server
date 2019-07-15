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
    return jwt.sign(header, payload,secrets.get_jwt_secret()).decode('utf8')  # the token is already b64 url encoded


def get_header_jwt(headers):
    if headers.get('Authorization'):
        athorization = headers.get('Authorization').split(' ')
        if len(athorization) == 2:
            return athorization[1].encode('utf8')


def user_authorized(headers):
    json_web_token = get_header_jwt(headers)
    try:
        if json_web_token:
            return jwt.verify(json_web_token, secrets.get_jwt_secret())
    except jwt.JwtInvalidSignatureError:
        return None

