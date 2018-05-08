import sqlite3
import settings

class DatabaseManager:

    def __init__(self, mailing_list):
        path = settings.STEPOUT_BASE_PATH + mailing_list + ".db"
        with sqlite3.connect(path) as conn:
            self.cursor = conn.cursor()

    def store_item(self, item):
        pass