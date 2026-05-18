import sqlite3

from claims_automation.config import DATABASE_PATH, SCHEMA_PATH


def create_database():
    """Create the SQLite database using the schema.sql file."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(database=DATABASE_PATH) as connection:
        connection.executescript(schema_sql)

    print(f"Database created at: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
