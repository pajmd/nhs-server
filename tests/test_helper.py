from app.utils import helper


def test_get_password_hash():
    pwd_test = 'I am not a good password!'
    pwd_test2 = 'I am different not a good password!'
    salt = helper.get_salt()
    hashed_pwd = helper.get_password_hash(pwd_test, salt)
    hashed_pwd2 = helper.get_password_hash(pwd_test2, salt)
    assert hashed_pwd != hashed_pwd2


def test_get_salt():
    salt = helper.get_salt()
    assert len(salt) == 16
    salt2 = helper.get_salt()
    assert salt != salt2
