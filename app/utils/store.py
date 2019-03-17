import pymongo
import datetime

MONGO_URI = 'mongodb://127.0.0.1:27017/'
MONGO_DATABASE = 'nhsdb'


class StoreUserAlreadyExists(Exception):
    pass


class StoreUserNotFound(Exception):
    pass


class MongoStore(object):
    collection_name = 'nhsUsers'

    def __init__(self, mongo_uri, mongo_db, validate=None, validation_schema=None):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.validate = validate
        self.validation_schema = validation_schema

    def open_db(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if self.validate:
            self.apply_validation()

    def apply_validation(self):
        if self.collection_name in self.db.collection_names():
            self.db.runCommand({
                'collMod': self.collection_name,
                'validator': self.validation_schema
            }
            )
        else:
            self.db.createCollection(self.collection_name, **self.validation_schema)

    def close_db(self, spider):
        self.client.close()

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
            match = self.db[self.collection_name].find_one({
                'email': user['email']
            })
            if not match:
                user['create_ts'] = datetime.datetime.utcnow()
                user['update_ts'] = datetime.datetime.utcnow()
                id = self.db[self.collection_name].insert_one(user).inserted_id
                return id
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
