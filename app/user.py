from app.utils.helper import get_password_hash, get_salt
from app.db.userstore import UserStore
from app.db.store import MONGO_URI, MONGO_DATABASE


# need to add context with to close db
class User(object):
    def __init__(self, user):
        self.user = user

    def create_user(self):
        salt = get_salt()
        hashed_password = get_password_hash(self.user['password'], get_salt())
        # user:
        # {
        #   'email': email@address,
        #   'hash': hash,
        #   'salt': salt,
        #   'first_name': firstname
        #   'last_name': lastname
        # }
        self.user['hash'] = hashed_password
        self.user['salt'] = salt
        self.user['first_name'] = self.user.get('first_name', 'unknown first name')
        self.user['last_name'] = self.user.get('last_name', 'unknown last name')
        with UserStore(MONGO_URI, MONGO_DATABASE) as user_store:
            user_store.add_user(self.user)

    def update(self):
        pass

    def delete(self):
        pass

    def get_user(self):
        pass
