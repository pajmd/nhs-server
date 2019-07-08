from app.utils.helper import get_password_hash, get_salt
from app.db.userstore import UserStore, StoreUserAlreadyExists, StoreUserNotFound
from app.db.store import MONGO_URI, MONGO_DATABASE


class UserAlreadyExists(Exception):
    pass


class UserCreateError(Exception):
    pass


class UserFindError(Exception):
    pass


# need to add context with to close db
class User(object):
    def __init__(self, user, mongo_uri=MONGO_URI, mongo_database=MONGO_DATABASE):
        self.user = user
        self.mongo_uri = mongo_uri
        self.mongo_database = mongo_database

    def create_user(self):
        salt = get_salt()
        hashed_password = get_password_hash(self.user['password'], salt)
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
        with UserStore(self.mongo_uri, self.mongo_database) as user_store:
            try:
                self.user.pop('password')
                return user_store.add_user(self.user)
            except StoreUserAlreadyExists as e:
                raise UserAlreadyExists(str(e))
            except Exception as e:
                raise UserCreateError(str(e))

    def update(self):
        pass

    def delete(self):
        pass

    def get_user_by_email(self):
        with UserStore(self.mongo_uri, self.mongo_database) as user_store:
            return user_store.get_user(self.user)

    def authenticate_user(self):
        """returns None if user not authenticated"""
        with UserStore(self.mongo_uri, self.mongo_database) as user_store:
            try:
                stored_user = user_store.get_user(self.user)
                if stored_user:
                    hashed_password = get_password_hash(self.user['password'], stored_user['salt'])
                    if hashed_password == stored_user['hash']:
                        return self.public_user(stored_user)
            except StoreUserNotFound as e:
                raise UserFindError(e)

    @staticmethod
    def public_user(user):
        public_usr = user.copy()
        public_usr.pop('hash', None)
        public_usr.pop('salt', None)
        public_usr['_id'] = str(public_usr['_id'])
        return public_usr
