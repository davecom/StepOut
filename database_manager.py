import sqlite3
import settings


class DatabaseManager:

    def __init__(self, mailing_list):
        path = settings.STEPOUT_BASE_PATH + mailing_list + ".db"
        with sqlite3.connect(path) as conn:
            self.conn = conn
            self.cursor = conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, address TEXT, date TEXT, subject TEXT, content TEXT)")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def store_item(self, item):
        self.cursor.execute("INSERT INTO messages(sender, address, date, subject, content) VALUES (?, ?, ?, ?, ?)", (item.sender, item.address, item.date, item.subject, item.content))
        self.conn.commit()