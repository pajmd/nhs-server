import jwt


class JwtExpiredSignatureError(Exception):
    pass


class JwtMissingRequiredClaimError(Exception):
    pass

def sign(header, payload, secret):
    """signs the header and payloads. Returna JWT object
    header = {
    "typ": "JWT",
    "alg": "HS256"
    }
    payload = {
     "iat": 1422779638,
     "exp": 1623780638,
    "userId": "b08f86af-35da-48f2-8fab-cef3904660bd",
    "name": "fiest name last name"
    }
    """
    token = jwt.encode(payload=payload, headers=header, key=secret, algorithm='HS256')
    return token


def verify(jwt_token, secret):
    """Verifies the token. Returns True if valid"""
    try:
        payload = jwt.decode(jwt_token, secret, algorithms=['HS256'],
                             options={
                                 'require_exp': True,
                                 'verify_exp': True,
                                 'require_iat': True,
                                 'verify_iat': True
                             })
        return payload

    except jwt.ExpiredSignatureError:
        raise JwtExpiredSignatureError('Signature has expired')
    except jwt.MissingRequiredClaimError as ex:
        raise JwtMissingRequiredClaimError(str(ex))
