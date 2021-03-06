from app.db.store import MongoStore, StoreConnectionError
import datetime
import logging

logger = logging.getLogger("%s.%s" % ('nhs-app', __name__))


COLLECTION_NAME = 'nhsUsers'


class StoreUserAlreadyExists(Exception):
    pass


class StoreUserNotFound(Exception):
    pass


class UserStore(MongoStore):

    def __init__(self, mongo_uri, mongo_db, validate=False, validation_schema=None):
        super(UserStore, self).__init__(mongo_uri, mongo_db, COLLECTION_NAME)
        self.validate = validate
        self.validation_schema = validation_schema

    def __enter__(self):
        self.open_db()
        if self.validate:
            self.apply_validation(self.validation_schema)
        return self

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
        except Exception as ex:
            logger.info("Failed adding user %s - %s" % (user, ex))
            raise
        if not match:
            user['create_ts'] = datetime.datetime.utcnow()
            user['update_ts'] = datetime.datetime.utcnow()
            user_id = self.db[self.collection_name].insert_one(user).inserted_id
            user['_id'] = user_id
            return user
        else:
            raise StoreUserAlreadyExists('%s already exists' % user['email'])

    def get_user(self, user, hashed_password=None):
        """get a user, the key being its unique email address"""
        # user:
        # {
        #   'email': email@address,
        #   'hash': hash,
        #   'salt': salt,
        #   'first_name': firstname
        #   'last_name': lastname
        # }
        try:
            return self.find_one({
                    'email': user['email']
                })
        except StoreConnectionError as e:
            raise StoreUserNotFound("Connection error: %s" % str(e))

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
            logger.info("Failed updatating user %s - %s" % (user, ex))
            raise

    def delete_user(self, user):
        # user:
        # {
        #   'email': email@address
        # }

        try:
            match = self.db[self.collection_name].find_one(user)
            if match:
                self.db[self.collection_name].delete_one(
                    {
                        '_id': match['_id']
                    })
            else:
                raise StoreUserNotFound('%s already exists' % user['email'])
        except Exception as ex:
            logger.info("Failed deleting user %s - %s" % (user, ex))
            raise
