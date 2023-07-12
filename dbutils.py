import sqlite3

def db_setup():
    with sqlite3.connect("hymns.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")
        query = """CREATE TABLE IF NOT EXISTS services (
            services_id INTEGER PRIMARY KEY,
            service_date TEXT NOT NULL,
            type NOT NULL,
            event TEXT) WITHOUT ROWID;"""
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS songs (
                title TEXT,
                verse TEXT,
                chorus TEXT,
                bridge TEXT
                );"""
        cursor.execute(query)


        query = """CREATE TABLE IF NOT EXISTS hymnals(
                hymnal_id TEXT PRIMARY KEY,
                full_title TEXT
                ) WITHOUT ROWID;"""
        cursor.execute(query)


        query = """ CREATE TABLE IF NOT EXISTS selections (
                hymnal_id TEXT,
                song_id INTEGER,
                service_id INTEGER,
                position TEXT,
                PRIMARY KEY (hymnal_id, song_id, service_id),
                FOREIGN KEY(hymnal_id) REFERENCES hymnal(hymnal_id),
                FOREIGN KEY(song_id) REFERENCES songs(rowid),
                FOREIGN KEY(service_id) REFERENCES service(service_id)
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS arrangements(
                hymnal_id TEXT,
                song_id INTEGER,
                number INTEGER,
                order_str TEXT,
                title TEXT,
                PRIMARY KEY (hymnal_id, song_id),
                FOREIGN KEY(hymnal_id) REFERENCES hymnal(hymnal_id),
                FOREIGN KEY(song_id) REFERENCES songs(rowid)
                ) WITHOUT ROWID;"""

        cursor.execute(query)
        conn.commit()

def add_song(verse: str = "", chorus: str = "", bridge: str = "") -> None:
    with sqlite3.connect("hymns.db") as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO songs VALUES ('{verse}', '{chorus}', '{bridge}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from songs")
        print(res.fetchall())
        
if __name__ == "__main__":
    add_song(chorus="this is a test chorus", verse="some verses would go here")
