from app.db.store import MongoStore, MONGO_URI
import datetime
import pytest
from pymongo import errors

TEST_DB = 'test_nhsdb'
TEST_COLLECTION = 'test_users'


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
