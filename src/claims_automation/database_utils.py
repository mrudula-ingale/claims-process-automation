import sqlite3

from claims_automation.config import DATABASE_PATH


def get_database_connection() -> sqlite3.Connection:
    """
    Create and return SQLite database connection.
    """
    return sqlite3.connect(DATABASE_PATH)
