import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "claims.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"


def create_database():
    """Create the SQLite database using the schema.sql file."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(database=DATABASE_PATH) as connection:
        connection.executescript(schema_sql)

    print(f"Database created at: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()
