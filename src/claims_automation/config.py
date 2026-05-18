from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = DATA_DIR / "reports"

SQL_DIR = PROJECT_ROOT / "sql"

DATABASE_PATH = DATA_DIR / "claims.db"

SCHEMA_PATH = SQL_DIR / "schema.sql"
