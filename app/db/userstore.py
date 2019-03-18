from app.db.store import MongoStore
import datetime


COLLECTION_NAME = 'nhsUsers'


class StoreUserAlreadyExists(Exception):
    pass


class StoreUserNotFound(Exception):
    pass


class UserStore(MongoStore):

    def __init__(self, mongo_uri, mongo_db, validate=False, validation_schema=None):
        super(MongoStore, self).__init__(mongo_uri, mongo_db, COLLECTION_NAME)
        self.validate = validate
        self.validation_schema = validation_schema

    def __enter__(self):
        self.open_db()
        if self.validate:
            self.apply_validation(self.validation_schema)

    def __exit__(self, *args):
        self.close_db()

    def add_user(self, user):
        # user:
        # {
        #   'email': email@address,
        #   'hash': hash,
        #   'salt': salt,
        #   'first_name': firstname
        #   'last_name': lastname
        # }

        try:
            match = self.find_one({
                'email': user['email']
            })
            if not match:
                user['create_ts'] = datetime.datetime.utcnow()
                user['update_ts'] = datetime.datetime.utcnow()
                user_id = self.db[self.collection_name].insert_one(user).inserted_id
                return user_id
            else:
                raise StoreUserAlreadyExists('%s already exists' % user['email'])
        except Exception as ex:
            print("Failed adding user %s - %s" % (user, ex))
            raise

    def update_user(self, user):
        # user:
        # {
        #   'email': email@address
        # }

        try:
            match = self.db[self.collection_name].find_one(user)
            if match:
                user['update_ts'] = datetime.datetime.utcnow()
                res = self.db[self.collection_name].update_one(
                    {
                        '_id': match['_id']
                    },
                    user,
                    upsert=False)
            else:
                raise StoreUserNotFound('%s already exists' % user['email'])
        except Exception as ex:
            print("Failed updatating user %s - %s" % (user, ex))
            raise

    def delete_user(self, user):
        # user:
        # {
        #   'email': email@address
        # }

        try:
            match = self.db[self.collection_name].find_one(user)
            if match:
                res = self.db[self.collection_name].delete_one(
                    {
                        '_id': match['_id']
                    })
            else:
                raise StoreUserNotFound('%s already exists' % user['email'])
        except Exception as ex:
            print("Failed deleting user %s - %s" % (user, ex))
            raise
