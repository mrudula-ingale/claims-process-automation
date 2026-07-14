import os
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

SQL_DIR = PROJECT_ROOT / "sql"
QUERIES_DIR = SQL_DIR / "queries"

DEFAULT_DATABASE_PATH = DATA_DIR / "claims.db"

if str(PROJECT_ROOT).startswith("/mount/src/"):
    DEFAULT_DATABASE_PATH = (
        Path(tempfile.gettempdir()) / "claims-process-automation" / "claims.db"
    )

DATABASE_PATH = Path(os.environ.get("CLAIMS_DATABASE_PATH", DEFAULT_DATABASE_PATH))
DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("CLAIMS_DATABASE_URL")
SCHEMA_PATH = SQL_DIR / "schema.sql"

KPI_REPORT_PATH = REPORTS_DIR / "claims_kpi_report.xlsx"
