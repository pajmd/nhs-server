import pymongo
import logging
import os


#logger = logging.getLogger("%s.%s" % ('nhs-app', __name__))
logger = logging.getLogger()


def get_mongo_uri():
    mongo_host = os.environ.get('MONGO_HOST', "127.0.0.1")
    mongo_port = os.environ.get('MONGO_PORT', '27017')
    mongo_relpset = os.environ.get('MONGO_REPLSET')
    hosts = [host.strip(' ') for host in mongo_host.split(',')]
    ports = [port.strip(' ') for port in mongo_port.split(',')]
    if len(hosts) == len(ports):
        uri = ",".join(["%s:%s" % (host, port) for (host, port) in zip(hosts, ports)])
    elif len(ports) == 1:
        uri = ",".join(["%s:%s" % (host, mongo_port) for host in hosts])
    else:
        raise Exception("Error: mismatched between mongo hosts (%s) and ports (%s)" % (mongo_host, mongo_port))
    if mongo_relpset:
        uri = 'mongodb://%s/replicaSet=%s' % (uri, mongo_relpset)
    else:
        uri = 'mongodb://%s/' % uri
    return uri


MONGO_URI = get_mongo_uri()
MONGO_DATABASE = 'nhsdb'


class StoreConnectionError(Exception):
    pass


class MongoStore(object):

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    def open_db(self):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
        except Exception as e:
            logger.error(e)
            raise

    def apply_validation(self, validation_schema):
        if self.collection_name in self.db.list_collection_names():
            self.db.command({
                'collMod': self.collection_name,
                'validator': validation_schema
            }
            )
        else:
            # self.db.createCollection(self.collection_name, **validation_schema)
            self.db.create_collection(self.collection_name)
            self.db.command({
                'collMod': self.collection_name,
                'validator': validation_schema
            }
            )

    def close_db(self):
        self.client.close()

    def find_one(self, criteria):
        try:
            match = self.db[self.collection_name].find_one(criteria)
            return match
        except pymongo.mongo_client.ServerSelectionTimeoutError as e:
            logger.error("Could not find %s - error: %s" % (criteria, str(e)))
            raise StoreConnectionError(e)
        except Exception as e:
            logger.error("Could not find %s - error: %s" % (criteria, str(e)))
            raise StoreConnectionError(e)

    def insert_one(self, document):
        return self.db[self.collection_name].insert_one(document).inserted_id

