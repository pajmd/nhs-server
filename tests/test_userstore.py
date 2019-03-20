from app.db import userstore
import datetime
import pytest


MONGO_URI = 'mongodb://127.0.0.1:27017/'
MONGO_DATABASE = 'test_nhsdb'


def test_add_user(start_mongo_no_existing_collection_db):
    with userstore.UserStore(MONGO_URI, MONGO_DATABASE) as store:
        user = {
            'email': "usr@address",
            'hash': "hash",
            'salt': "salt",
            'first_name': "firstname",
            'last_name': "lastname",
            'create_ts': datetime.datetime.utcnow(),
            'update_ts': datetime.datetime.utcnow()
        }
        store.add_user(user)


def test_user_already_exists(start_mongo_no_existing_collection_db):
    with userstore.UserStore(MONGO_URI, MONGO_DATABASE) as store:
        user = {
            'email': "usr@address",
            'hash': "hash",
            'salt': "salt",
            'first_name': "firstname",
            'last_name': "lastname",
            'create_ts': datetime.datetime.utcnow(),
            'update_ts': datetime.datetime.utcnow()
        }
        store.add_user(user)
    with pytest.raises(userstore.StoreUserAlreadyExists):
        with userstore.UserStore(MONGO_URI, MONGO_DATABASE) as store2:
            user = {
                'email': "usr@address",
                'hash': "hash",
                'salt': "salt",
                'first_name': "firstname",
                'last_name': "lastname",
                'create_ts': datetime.datetime.utcnow(),
                'update_ts': datetime.datetime.utcnow()
            }
            store2.add_user(user)


