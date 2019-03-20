

function connect_db_drop_collection() {
    var conn = new Mongo();
    var db = conn.getDB('test_nhsdb')
    db.nhsUsers.drop()
}

connect_db_drop_collection()