import os


SOLR_HOST = "SOLR_HOST"
SOLR_PORT = "SOLR_PORT"
SOLR_COLLECTION = "SOLR_COLLECTION"


solr = {
    "SOLR_HOST": os.environ.get(SOLR_HOST, 'localhost'),
    "SOLR_PORT": os.environ.get(SOLR_PORT, 8983),
    "SOLR_COLLECTION": os.environ.get(SOLR_COLLECTION, 'nhsCollection')
}


def get_solr_uri(host, port):
    uri = "http://{host}:{port}".format(host=host, port=port)
    return uri


def get_collection_url(collection):
    query = "solr/{collection}/select?q".format(collection=collection)
    return query

def get_url():
    return "{uri}/{collection_url}".format(
        uri=get_solr_uri(solr.get(SOLR_HOST), solr.get(SOLR_PORT)),
        collection_url=get_collection_url(solr.get(SOLR_COLLECTION)))


def get_solr_query(payload):
    return "{uri}/{collection_url}={payload}".format(
        uri=get_solr_uri(solr.get(SOLR_HOST), solr.get(SOLR_PORT)),
        collection_url=get_collection_url(solr.get(SOLR_COLLECTION)),
        payload=payload
    )