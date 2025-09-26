import glob
import logging
import os
import sqlite3
from contextlib import contextmanager

import config


class Database:
    def __init__(self, path="database/database.sqlite3"):
        self.db_path = config.DB_PATH or path
        self._init_db()

    def _init_db(self):
        with self.connect() as connection:
            connection.execute("pragma journal_mode=wal")
            cursor = connection.cursor()
            cursor.executescript("""
                -- Create migrations history table.
                create table if not exists migrations (
                    id integer primary key autoincrement,
                    script text not null,
                    executed_at timestamp not null default current_timestamp
                );

                -- Insert an entry into that table to kick off
                -- the autoincrement
                insert into migrations (id, script)
                select 0, 'init'
                where not exists (
                    select 1
                    from migrations
                    where script = 'init'
                );
            """)
            connection.commit()

    def _add_migration(self, migration):
        logging.info(f"Adding {migration}...")
        migration_script = None
        with open(migration, "r") as f:
            migration_script = f.read()

        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.executescript(migration_script)
            cursor.execute(
                """
                insert into migrations (script)
                values (
                    :migration
                );
            """,
                (migration,),
            )
            connection.commit()
            logging.info(f"{migration} added successfully.")

    def migrate(self):
        migrated = ()
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                select id, script, executed_at
                from migrations
                order by executed_at;
            """)
            migrated = set([row["script"] for row in cursor.fetchall()])

        migrations = sorted(glob.glob("app/db/migrations/*.sql"))
        for migration in migrations:
            if migration not in migrated:
                self._add_migration(migration)

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
