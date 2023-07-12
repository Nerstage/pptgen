import sqlite3

con = sqlite3.connect("hymns.db")
con.execute("PRAGMA foreign_keys = ON")
query = """CREATE TABLE IF NOT EXISTS services (
        services_id INTEGER PRIMARY KEY,
        service_date TEXT NOT NULL,
        type NOT NULL,
        event TEXT) WITHOUT ROWID;"""
con.execute(query)

query = """ CREATE TABLE IF NOT EXISTS songs (
        song_id INTEGER PRIMARY KEY,
        verse TEXT,
        chorus TEXT,
        bridge TEXT
        ) WITHOUT ROWID;"""
con.execute(query)


query = """CREATE TABLE IF NOT EXISTS hymnals(
        hymnal_id TEXT PRIMARY KEY,
        full_title TEXT
        ) WITHOUT ROWID;"""
con.execute(query)


query = """ CREATE TABLE IF NOT EXISTS selections (
        hymnal_id TEXT,
        song_id INTEGER,
        service_id INTEGER,
        position TEXT,
        PRIMARY KEY (hymnal_id, song_id, service_id),
        FOREIGN KEY(hymnal_id) REFERENCES hymnal(hymnal_id),
        FOREIGN KEY(song_id) REFERENCES songs(song_id),
        FOREIGN KEY(service_id) REFERENCES service(service_id)
        );"""
con.execute(query)

query = """CREATE TABLE IF NOT EXISTS arrangements(
        hymnal_id TEXT,
        song_id INTEGER,
        number INTEGER,
        order_str TEXT,
        PRIMARY KEY (hymnal_id, song_id)
        ) WITHOUT ROWID;"""
con.execute(query)

con.commit()
con.close()
