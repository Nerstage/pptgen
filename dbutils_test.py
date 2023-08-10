import unittest, sqlite3
from dbutils import *


class TestAdds(unittest.TestCase):
    def setUp(self) -> None:
        db_setup(db="test.db")

    def tearDown(self) -> None:
        os.remove("test.db")

    def test_hymnals(self):
        add_hymnal("UMH", "United Methodist Hymnal", db="test.db")
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            query = "SELECT hymnal_id, full_title FROM hymnals"
            cursor.execute(query)
            res = cursor.fetchall()
        self.assertEqual(res, [("UMH", "United Methodist Hymnal")])

    def test_songs(self):
        add_song("some song", "verse1 jfdk;a", "chorus fjkdfj", "", db="test.db")
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            query = "SELECT title, verse, chorus, bridge FROM songs"
            cursor.execute(query)
            res = cursor.fetchall()
        self.assertEqual(res, [("some song", "verse1 jfdk;a", "chorus fjkdfj", "")])

    def test_services(self):
        add_service("2023-01-01", "Sunday", db="test.db")
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            query = "SELECT service_date, service_type, event FROM services"
            cursor.execute(query)
            res = cursor.fetchall()
        self.assertEqual(res, [("2023-01-01", "Sunday", "")])

    def test_arrangement(self):
        add_hymnal("UMH", "United Methodist Hymnal", db="test.db")
        add_song("some song", "verse1 jfdk;a", "chorus fjkdfj", "", db="test.db")
        add_arrangement(
            11, "vc", "title", hymnal_id="UMH", song_title="some song", db="test.db"
        )
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            query = (
                "SELECT hymnal_id, song_id, number, order_str, title FROM arrangements"
            )
            cursor.execute(query)
            res = cursor.fetchall()
        self.assertEqual(res, [("UMH", 1, 11, "vc", "title")])

    def test_selection(self):
        add_hymnal("UMH", "United Methodist Hymnal", db="test.db")
        add_song("some song", "verse1 jfdk;a", "chorus fjkdfj", "", db="test.db")
        add_service("2023-01-01", "Sunday", db="test.db")
        add_selection(1, 1, hymnal_id="UMH", song_title="some song", db="test.db")
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            query = "SELECT hymnal_id, song_id, service_id, position FROM selections"
            cursor.execute(query)
            res = cursor.fetchall()
        self.assertEqual(res, [("UMH", 1, 1, 1)])


if __name__ == "__main__":
    unittest.main()
