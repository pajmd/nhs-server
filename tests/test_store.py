from app.db.store import MongoStore, MONGO_URI, get_mongo_uri
import datetime
import pytest
from pymongo import errors

TEST_DB = 'test_nhsdb'
TEST_COLLECTION = 'test_users'


@pytest.mark.parametrize('mongo_host, mongo_port,mongo_replset, expected',[
    ('1.1.1.1', None, None, 'mongodb://1.1.1.1:27017/'),
    ('1.1.1.1', '1111', None,  'mongodb://1.1.1.1:1111/'),
    ('1.1.1.1', '2222', 'rs2', 'mongodb://1.1.1.1:2222/replicaSet=rs2'),
    ('1.1.1.1, 2.2.2.2, 3.3.3.3  ', ' 111, 2222 , 3333 ', None, 'mongodb://1.1.1.1:111,2.2.2.2:2222,3.3.3.3:3333/'),
    ('1.1.1.1, 2.2.2.2', None, 'rs4', 'mongodb://1.1.1.1:27017,2.2.2.2:27017/replicaSet=rs4'),
    ('1.1.1.1, 2.2.2.2', '555', None, 'mongodb://1.1.1.1:555,2.2.2.2:555/')
])
def test_mongo_uri(mongo_host, mongo_port,mongo_replset, expected):
    import os

    def clear_env():
        for v in ['MONGO_HOST', 'MONGO_PORT', 'MONGO_REPLSET']:
            if v in os.environ:
                del os.environ[v]

    clear_env()
    os.environ
    if mongo_host:
        os.environ['MONGO_HOST'] = mongo_host
    if mongo_port:
        os.environ['MONGO_PORT'] = mongo_port
    if mongo_replset:
        os.environ['MONGO_REPLSET'] = mongo_replset
    assert get_mongo_uri() == expected


def test_start_mongo_no_existing_collection_db(start_mongo_no_existing_collection_db):
    pass


def test_start_mongo_add_test_users_collection_db(start_mongo_add_test_users_collection_db):
    pass


def test_open_db():
    mongo_store = MongoStore(MONGO_URI, TEST_DB, TEST_COLLECTION)
    mongo_store.open_db()
    mongo_store.close_db()


#   'email': email@address,
#   'hash': hash,
#   'salt': salt,
#   'first_name': firstname
#   'last_name': lastname

def test_validation(start_mongo_no_existing_collection_db):
    VALIDATION_SCHEMA = {
        '$jsonSchema': {
            'bsonType': "object",
            'required': ["email", "first_name", "last_name", "hash", "salt", "create_ts", "update_ts"],
            'properties': {
                'email': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'first_name': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'last_name': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'hash': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'salt': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'create_ts': {
                    'bsonType': "date",
                    'description': "must be a date and is required"
                },
                'update_ts': {
                    'bsonType': "date",
                    'description': "must be a date and is required"
                }
            }
        }
    }
    mongo_store = MongoStore(MONGO_URI, TEST_DB, TEST_COLLECTION)
    mongo_store.open_db()
    mongo_store.apply_validation(VALIDATION_SCHEMA)
    mongo_store.close_db()


def test_exisitng_collection_validation(start_mongo_add_test_users_collection_db):
    VALIDATION_SCHEMA = {
        '$jsonSchema': {
            'bsonType': "object",
            'required': ["email", "first_name", "last_name", "hash", "salt", "create_ts", "update_ts"],
            'properties': {
                'email': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'first_name': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'last_name': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'hash': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'salt': {
                    'bsonType': "string",
                    'description': "must be a string and is required"
                },
                'create_ts': {
                    'bsonType': "date",
                    'description': "must be a date and is required"
                },
                'update_ts': {
                    'bsonType': "date",
                    'description': "must be a date and is required"
                }
            }
        }
    }
    mongo_store = MongoStore(MONGO_URI, TEST_DB, TEST_COLLECTION)
    mongo_store.open_db()
    mongo_store.apply_validation(VALIDATION_SCHEMA)
    mongo_store.close_db()


def test_insert_one(start_mongo_add_test_users_collection_db):
    user = {
        'email': "email@address",
        'hash': "hash",
        'salt': "salt",
        'first_name': "firstname",
        'last_name': "lastname",
        'create_ts': datetime.datetime.utcnow(),
        'update_ts': datetime.datetime.utcnow()
    }
    mongo_store = MongoStore(MONGO_URI, TEST_DB, TEST_COLLECTION)
    mongo_store.open_db()
    mongo_store.insert_one(user)
    mongo_store.close_db()


def test_missing_required_insert_one():
    user = {
        'email': 1234,
        'hash': "hash",
        'salt': "salt",
        'first_name': "firstname",
        'last_name': "lastname",
        'create_ts': datetime.datetime.utcnow(),
        'update_ts': datetime.datetime.utcnow()
    }
    mongo_store = MongoStore(MONGO_URI, TEST_DB, TEST_COLLECTION)
    mongo_store.open_db()
    with pytest.raises(errors.WriteError):
        mongo_store.insert_one(user)
    mongo_store.close_db()
