from app.utils.helper import get_password_hash, get_salt
from app.utils import store

# need to add context with to close db
class User(object):
    def __init__(self, user):
        self.user = user
        db = store.MongoStore(store.MONGO_URI, store.MONGO_DATABASE)
        self.client_db = db.open_db()

    def create_user(self):
        salt = get_salt()
        hash = get_password_hash(self.user['password'], get_salt())
        # user:
        # {
        #   'email': email@address,
        #   'hash': hash,
        #   'salt': salt,
        #   'first_name': firstname
        #   'last_name': lastname
        # }
        self.user['hash'] = hash
        self.user['salt'] = salt
        self.user['first_name'] = self.user.get('first_name', 'unknown first name')
        self.user['lasst_name'] = self.user.get('last_name', 'unknown last name')
        self.client_db.add_user(self.user)

    def update(self):
        pass

    def delete(self):
        pass

    def get_user(self):
        pass