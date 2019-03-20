
function connect_db_add_collection(collection) {
    var conn = new Mongo();
    var db = conn.getDB('test_nhsdb')
    db.createCollection(collection)
}

connect_db_add_collection('nhsUsers')