from app.utils import jwt
import pytest


secret = "your-256-bit-secret"


def test_sign():
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
    expected_token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE0MjI3Nzk2MzgsImV4cCI6MTYyMzc4MDYzOCwidXNlcklkIjoiYjA4Zjg2YWYtMzVkYS00OGYyLThmYWItY2VmMzkwNDY2MGJkIiwibmFtZSI6ImZpZXN0IG5hbWUgbGFzdCBuYW1lIn0.xkqhqDmvTXRLkAq47BF1edsFUb2lTemMoMwvozY7VEo"
    token = jwt.sign(header, payload, secret)
    assert token == expected_token


def test_verify():
    jwt_token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE0MjI3Nzk2MzgsImV4cCI6MTYyMzc4MDYzOCwidXNlcklkIjoiYjA4Zjg2YWYtMzVkYS00OGYyLThmYWItY2VmMzkwNDY2MGJkIiwibmFtZSI6ImZpZXN0IG5hbWUgbGFzdCBuYW1lIn0.xkqhqDmvTXRLkAq47BF1edsFUb2lTemMoMwvozY7VEo"
    payload = jwt.verify(jwt_token, secret)
    assert payload["name"] == "fiest name last name"


def test_verify_expired():
    jwt_token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE0MjI3Nzk2MzgsImV4cCI6MTQyMjc3OTYzOCwidXNlcklkIjoiYjA4Zjg2YWYtMzVkYS00OGYyLThmYWItY2VmMzkwNDY2MGJkIiwibmFtZSI6ImZpZXN0IG5hbWUgbGFzdCBuYW1lIn0.HdKN-cQMZZLlT69X9Mt8H7SXldtCi_NXso6U3UHBx7U"
    with pytest.raises(jwt.JwtExpiredSignatureError):
        payload = jwt.verify(jwt_token, secret)


def test_verify_missing_claim():
    jwt_token = b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjM3ODA2MzgsInVzZXJJZCI6ImIwOGY4NmFmLTM1ZGEtNDhmMi04ZmFiLWNlZjM5MDQ2NjBiZCIsIm5hbWUiOiJmaWVzdCBuYW1lIGxhc3QgbmFtZSJ9.m-lTRNjqTaOP85pOLCy49RfSX8icJb2mFm1OFq2Usrk"
    with pytest.raises(jwt.JwtMissingRequiredClaimError) as e:
        payload = jwt.verify(jwt_token, secret)
    print(e)
