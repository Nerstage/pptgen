import sqlite3

default_db = "hymns.db"

def db_setup(db: str = default_db):
    with sqlite3.connect(default_db) as conn:
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = ON")
        query = """CREATE TABLE IF NOT EXISTS services (
                service_date TEXT NOT NULL,
                service_type NOT NULL,
                event TEXT
                );"""
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
                FOREIGN KEY(service_id) REFERENCES service(rowid)
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

def add_song(verse: str = "", chorus: str = "", bridge: str = "", db: str = default_db) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO songs VALUES ('{verse}', '{chorus}', '{bridge}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from songs")
        print(res.fetchall())
        
def add_hymnal(code: str, title: str, db: str = default_db) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO hymnals VALUES ('{code}', '{title}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from hymnals")
        print(res.fetchall())

def add_service(service_date: str, service_type: str, event: str, db: str = default_db) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO services VALUES ('{service_date}', '{service_type}', '{event}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from services")
        print(res.fetchall())

if __name__ == "__main__":
    db_setup()
    #add_song(chorus="this is a test chorus", verse="some verses would go here")
    #add_hymnal(code="UMH", title="United Methodist Hymnal")
    add_service(service_date = "07/08/2022", service_type = "Sunday Morning", event = "None")
