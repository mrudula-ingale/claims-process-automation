import sqlite3
from pathlib import Path

import pandas as pd

from claims_automation.config import DATABASE_PATH, QUERIES_DIR


def load_sql_query(query_path: Path) -> str:
    """
    Read one SQL query file and return it as a string.

    Example:
    sql/queries/claims_by_status.sql
    """
    return query_path.read_text(encoding="utf-8")


def load_all_queries() -> dict[str, str]:
    """
    Load all SQL query files from sql/queries.

    Example:
    claims_by_status.sql -> "claims_by_status"
    """
    queries = {}

    for query_path in sorted(QUERIES_DIR.glob("*.sql")):
        report_name = query_path.stem
        queries[report_name] = load_sql_query(query_path)

    return queries


def execute_query(query: str) -> pd.DataFrame:
    """
    Execute one SQL query and return the result as a pandas DataFrame.
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(query, connection)


def execute_query_from_file(query_name: str) -> pd.DataFrame:
    """
    Execute a query by its filename.

    Example:
    execute_query_from_file("claims_by_status")
    """
    query_path = QUERIES_DIR / f"{query_name}.sql"

    query = load_sql_query(query_path)

    return execute_query(query)


def execute_all_queries() -> dict[str, pd.DataFrame]:
    """
    Execute all SQL query files and return results.

    Returns:
        {
            "claims_by_status": DataFrame,
            ...
        }
    """
    query_dictionary = load_all_queries()

    results = {}

    for report_name, query in query_dictionary.items():
        results[report_name] = execute_query(query)

    return results
