# this module should be replace by eh python 3.6 secrets module
import os


def token_bytes(n):
    return os.urandom(n)