import os
import sqlite3
from contextlib import contextmanager

import config


class Database:
    def __init__(self, path="database/database.sqlite3"):
        self.db_path = config.DB_PATH or path

    @contextmanager
    def connect(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        connection = sqlite3.connect(self.db_path, isolation_level=None)
        connection.row_factory = sqlite3.Row

        try:
            yield connection
        finally:
            connection.close()


db = Database()
