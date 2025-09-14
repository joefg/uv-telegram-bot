# Database

The database is a [SQLite](https://sqlite.org) database
with [WAL](https://www.sqlite.org/wal.html) enabled.

## Migrations

Migrations happen on startup.

To add a migration, add a SQL file to `migrations/`, following
the filename spec `<number>-<description>.sql`. The `number`
part is used to order the migrations at runtime.

### Gotchas

1. Don't forget your `if not exists` when making a new table.

2. Be careful of `returning *;`, depending on the size of the
migration you might max out your memory.
