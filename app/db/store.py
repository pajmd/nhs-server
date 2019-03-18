import pymongo

MONGO_URI = 'mongodb://127.0.0.1:27017/'
MONGO_DATABASE = 'nhsdb'


class MongoStore(object):

    def __init__(self, mongo_uri, mongo_db, collection_name, validation_schema=None):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    def open_db(self):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def apply_validation(self, validation_schema):
        if self.collection_name in self.db.collection_names():  # list_collection_names
            self.db.runCommand({
                'collMod': self.collection_name,
                'validator': validation_schema
            }
            )
        else:
            # self.db.createCollection(self.collection_name, **validation_schema)
            self.db.create_collection(self.collection_name)
            self.db.command({
                'collMod': self.collection_name,
                'validator': validation_schema['validator']
            }
            )

    def close_db(self):
        self.client.close()

    def find_one(self, criteria):
        match = self.db[self.collection_name].find_one(criteria)
        return match

    def insert_one(self, document):
        return self.db[self.collection_name].insert_one(document).inserted_id

