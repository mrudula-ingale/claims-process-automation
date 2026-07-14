import sqlite3

from sqlalchemy import create_engine, text

from claims_automation.config import DATABASE_PATH, DATABASE_URL, SCHEMA_PATH


def _schema_statements() -> list[str]:
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    return [
        statement.strip()
        for statement in schema_sql.split(";")
        if statement.strip()
    ]


def create_database() -> None:
    """Create the database using the schema.sql file."""
    if DATABASE_URL:
        engine = create_engine(DATABASE_URL)

        with engine.begin() as connection:
            for statement in _schema_statements():
                connection.execute(text(statement))

        print("Database schema created from DATABASE_URL.")
        return

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database=DATABASE_PATH) as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    print(f"Database created at: {DATABASE_PATH}")


def database_has_data() -> bool:
    """Return True when the claims table exists and contains rows."""
    query = "SELECT COUNT(*) FROM claims"

    try:
        if DATABASE_URL:
            engine = create_engine(DATABASE_URL)

            with engine.connect() as connection:
                count = connection.execute(text(query)).scalar_one()

            return count > 0

        if not DATABASE_PATH.exists():
            return False

        with sqlite3.connect(database=DATABASE_PATH) as connection:
            count = connection.execute(query).fetchone()[0]

        return count > 0
    except Exception:
        return False


def ensure_database() -> None:
    """Create and seed the database when it is missing or empty."""
    if database_has_data():
        return

    from claims_automation.generate_data import main as generate_data

    create_database()
    generate_data()


if __name__ == "__main__":
    create_database()
