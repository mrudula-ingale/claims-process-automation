import sqlite3

from claims_automation.config import DATABASE_PATH, SCHEMA_PATH


def create_database() -> None:
    """Create the SQLite database using the schema.sql file."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(database=DATABASE_PATH) as connection:
        connection.executescript(schema_sql)

    print(f"Database created at: {DATABASE_PATH}")


def ensure_database() -> None:
    """Create and seed the SQLite database when it is missing."""
    if DATABASE_PATH.exists():
        return

    from claims_automation.generate_data import main as generate_data

    create_database()
    generate_data()


if __name__ == "__main__":
    create_database()
