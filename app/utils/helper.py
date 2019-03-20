import hashlib, binascii
# to be replaced by python 3.6 secrets module
from app.utils import secrets


def get_password_hash(password, salt):
    dk = hashlib.pbkdf2_hmac('md5', password.encode('utf-8'), salt, 100000)
    return binascii.hexlify(dk)


def get_salt(n=16):
    return secrets.token_bytes(n)
