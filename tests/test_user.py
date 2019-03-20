from app.user import User
from app.db.userstore import UserStore

mongo_uri = 'mongodb://127.0.0.1:27017/'
mongo_database = 'test_nhsdb'


def test_create_user(start_mongo_no_existing_collection_db):

    user = {
      'email': 'email@address',
      'password': 'this is a password'
    }
    usr = User(user, mongo_uri, mongo_database)
    usr.create_user()
    with UserStore(mongo_uri, mongo_database) as user_store:
        stored_user = user_store.get_user(user)
        assert stored_user['email'] == user['email']
        assert stored_user['first_name'] == 'unknown first name'
        assert stored_user['last_name'] == 'unknown last name'
        assert len(stored_user['salt']) == 16
        assert stored_user.get('hash') is not None


def test_get_user_by_email(start_mongo_no_existing_collection_db):
    mongo_uri = 'mongodb://127.0.0.1:27017/'
    mongo_database = 'test_nhsdb'
    user = {
        'email': 'email@address',
        'password': 'this is a password',
        'first_name': 'laksa',
        'last_name': 'Thai food'
    }
    usr = User(user, mongo_uri, mongo_database)
    usr.create_user()
    stored_user = usr.get_user_by_email()
    assert stored_user['email'] == user['email']
    assert stored_user['first_name'] == user['first_name']
    assert stored_user['last_name'] == user['last_name']
    assert len(stored_user['salt']) == 16
    assert stored_user.get('hash') is not None


def test_get_non_existent_user(start_mongo_no_existing_collection_db):
    mongo_uri = 'mongodb://127.0.0.1:27017/'
    mongo_database = 'test_nhsdb'
    user = {
      'email': 'unknown_email@address',
      'password': 'this is a password'
    }
    usr = User(user, mongo_uri, mongo_database)
    stored_user = usr.get_user_by_email()
    assert stored_user is None
