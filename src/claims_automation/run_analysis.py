import pandas as pd

from claims_automation.config import KPI_REPORT_PATH, REPORTS_DIR
from claims_automation.query_manager import execute_all_queries


def export_results_to_excel(results: dict[str, pd.DataFrame]) -> None:
    """
    Export all query results into one Excel workbook.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(KPI_REPORT_PATH, engine="openpyxl") as writer:
        for sheet_name, dataframe in results.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excel report generated: {KPI_REPORT_PATH}")


def main() -> None:
    """
    Run automated SQL analysis pipeline.
    """
    results = execute_all_queries()

    export_results_to_excel(results)


if __name__ == "__main__":
    main()
