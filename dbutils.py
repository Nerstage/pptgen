import sqlite3
import os

default_db = "hymns.db"


def db_setup(db: str = default_db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")
        query = """CREATE TABLE IF NOT EXISTS services (
                service_id INTEGER PRIMARY KEY,
                service_date TEXT NOT NULL,
                service_type NOT NULL,
                event TEXT
                );"""
        cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY,
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
                position INTEGER,
                PRIMARY KEY (hymnal_id, song_id, service_id),
                FOREIGN KEY(hymnal_id) REFERENCES hymnals(hymnal_id),
                FOREIGN KEY(song_id) REFERENCES songs(song_id),
                FOREIGN KEY(service_id) REFERENCES services(service_id)
                );"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS arrangements(
                hymnal_id TEXT,
                song_id INTEGER,
                number INTEGER,
                order_str TEXT,
                title TEXT,
                PRIMARY KEY (hymnal_id, song_id),
                FOREIGN KEY(hymnal_id) REFERENCES hymnals(hymnal_id),
                FOREIGN KEY(song_id) REFERENCES songs(song_id)
                ) WITHOUT ROWID;"""

        cursor.execute(query)
        conn.commit()


def add_song(
    title: str,
    verse: str = "",
    chorus: str = "",
    bridge: str = "",
    db: str = default_db,
) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO songs (title, verse, chorus, bridge)\
              VALUES ('{title}', '{verse}', '{chorus}', '{bridge}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from songs")


def add_hymnal(hymnal_id: str, full_title: str, db: str = default_db) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO hymnals (hymnal_id, full_title)\
              VALUES ('{hymnal_id}', '{full_title}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from hymnals")


def add_service(
    service_date: str, service_type: str, event: str = "", db: str = default_db
) -> None:
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO services (service_date, service_type, event)\
              VALUES ('{service_date}', '{service_type}', '{event}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from services")


def add_selection(
    service_id: int,
    position: int = 0,
    hymnal_id: str = None,
    hymnal_title: str = None,
    song_id: int = None,
    song_title: str = None,
    db: str = default_db,
) -> None:
    if not hymnal_id:
        if not hymnal_title:
            raise Exception("A hymnal_id or hymnal_title must be provided.")
        hymnal_id = get_hymnal_id(hymnal_title, db=db)
    if not song_id:
        if not song_title:
            raise Exception("A song_id or song_title must be provided.")
        song_id = get_song_id(song_title, db=db)
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        query = f"INSERT INTO selections (hymnal_id, song_id, service_id, position)\
              VALUES ('{hymnal_id}', '{song_id}', '{service_id}', '{position}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from selections")


def add_arrangement(
    number: int,
    order_str: str,
    title: str,
    hymnal_id: str = None,
    hymnal_title: str = None,
    song_id: int = None,
    song_title: str = None,
    db: str = default_db,
) -> None:
    if not hymnal_id:
        if not hymnal_title:
            raise Exception("A hymnal_id or hymnal_title must be provided.")
        hymnal_id = get_hymnal_id(hymnal_title, db=db)
    if not song_id:
        if not song_title:
            raise Exception("A song_id or song_title must be provided.")
        song_id = get_song_id(song_title, db=db)
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        query = f"INSERT INTO arrangements (hymnal_id, song_id, number, order_str, title)\
              VALUES ('{hymnal_id}', '{song_id}', '{number}', '{order_str}', '{title}')"
        cursor.execute(query)
        conn.commit()
        res = cursor.execute("select * from arrangements")


def get_hymnal_id(full_title: str, db: str = default_db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = (
            f"SELECT hymnal_id, full_title FROM hymnals WHERE full_title='{full_title}'"
        )
        res = cursor.execute(query)
    for i in res:
        print(i)
        pick_hymnal = input("Choose this Hymnal? (y/n): ")
        if pick_hymnal.lower() == "y":
            return i[0]
    raise Exception("No results for this hymnal title!")


def get_song_id(title: str, db: str = default_db):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"SELECT song_id, title, verse, chorus, bridge FROM songs WHERE title='{title}'"
        cursor.execute(query)
        res = cursor.fetchall()
    if len(res) == 0:
        raise Exception("No results for this song title!")
    if len(res) == 1:
        return res[0][0]
    for i in res:
        print(i)
        pick_song = input("Choose this song? (y/n): ")
        if pick_song.lower() == "y":
            return i[0]


def get_service_id(
    service_date: str, service_type: str = None, event: str = None, db: str = default_db
):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        query = f"SELECT service_id, service_date, service_type, event FROM services WHERE service_date='{service_date}"
        if service_type:
            query = f"{query} AND service_type='{service_type}"
        if event:
            query = f"{query} AND event='{event}"
        cursor.execute(query)
        res = cursor.fetchall()
    if len(res) == 0:
        raise Exception("No results for services on this date!")
    if len(res) == 1:
        return res[0][0]
    for i in res:
        print(i)
        pick_service = input("Choose this service? (y/n): ")
        if pick_service.lower() == "y":
            return i[0]


if __name__ == "__main__":
    db_setup(db="test.db")
    try:
        add_hymnal("UMH", "United Methodist Hymnal", db="test.db")
    except:
        pass
    try:
        add_song("some song", "verse1 jfdk;a", "chorus fjkdfj", "", db="test.db")
    except:
        pass
    # add_arrangement(
    #     hymnal_title="United Methodist Hymnal",
    #     song_title="some song",
    #     number=100,
    #     order_str="vvc",
    #     title="song song",
    #     db = 'test.db'
    # )
    add_service("2023-01-01", "Sunday", db="test.db")
    os.remove("test.db")
