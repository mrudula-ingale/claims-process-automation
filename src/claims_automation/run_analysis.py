import sqlite3
from pathlib import Path

import pandas as pd

from claims_automation.config import (
    DATABASE_PATH,
    KPI_REPORT_PATH,
    QUERIES_DIR,
    REPORTS_DIR,
)


def load_sql_query(query_path: Path) -> str:
    """
    Read one SQL query file and return it as a string.

    Example:
    sql/queries/claims_by_status.sql
    """
    return query_path.read_text(encoding="utf-8")


def load_all_queries() -> dict[str, str]:
    """
    Load all .sql files from the queries folder.

    The filename becomes the report name.
    Example:
    claims_by_status.sql -> claims_by_status
    """
    queries = {}

    for query_path in sorted(QUERIES_DIR.glob("*.sql")):
        report_name = query_path.stem
        queries[report_name] = load_sql_query(query_path)

    return queries


def run_query(connection: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Execute one SQL query and return the result as a DataFrame.
    """
    return pd.read_sql_query(query, connection)


def run_all_queries() -> dict[str, pd.DataFrame]:
    """
    Run every SQL query file from sql/queries.
    """
    results = load_all_queries()

    with sqlite3.connect(DATABASE_PATH) as connection:
        for report_name, query in results.items():
            results[report_name] = run_query(connection, query)

    return results


def export_results_to_excel(results: dict[str, pd.DataFrame]) -> None:
    """
    Export query results into one Excel workbook.

    Each query result becomes one Excel sheet.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(KPI_REPORT_PATH, engine="openpyxl") as writer:
        for sheet_name, dataframe in results.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excel report generated: {KPI_REPORT_PATH}")


def main() -> None:
    """
    Run complete SQL automation pipeline.
    """
    results = run_all_queries()
    export_results_to_excel(results)


if __name__ == "__main__":
    main()
