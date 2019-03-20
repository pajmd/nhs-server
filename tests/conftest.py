import pytest
import subprocess


@pytest.fixture()
def start_mongo_no_existing_collection_db():
    subprocess.call(
        ["/usr/bin/mongo", "resources/connect_db_drop_collection.js"])


@pytest.fixture()
def start_mongo_add_test_users_collection_db():
    subprocess.call(
        ["/usr/bin/mongo", "resources/connect_db_add_test_users_collection.js"])

