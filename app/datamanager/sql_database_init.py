from team_lens_v1.app.logger import logger
from team_lens_v1.app.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_DB_PASSWORD, SUPABASE_URL_2, SUPABASE_DB_STRING
from supabase import Client, create_client
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

# supabase
SESSION_POOLER_SITE = (f"postgresql+psycopg2://postgres.{SUPABASE_DB_STRING}:{SUPABASE_DB_PASSWORD}"
                       f"@aws-1-eu-north-1.pooler.supabase.com:5432/postgres")
DIRECT_CONNECTION_SITE = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL_2}:5432/postgres"

# sqlite
# Get project root (where your main.py or run script is)
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Adjust based on file location
SQLITE_DB_DIR = PROJECT_ROOT / "data_storage" / "sql_db"
SQLITE_DB_PATH = SQLITE_DB_DIR / "team_lens.db"
SQLITE_PATH = f"sqlite:///{SQLITE_DB_PATH}"


def ensure_sqlite_db_exists(db_path: str) -> None:
    """
    Ensures the SQLite database file and its parent directory exist.
    """
    # Convert to Path object for easier manipulation
    db_file = Path(db_path)

    # Create parent directory if it doesn't exist
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Create empty database file if it doesn't exist
    if not db_file.exists():
        db_file.touch()
        logger.info(f"Created new SQLite database at {db_path}")
    else:
        logger.info(f"Using existing SQLite database at {db_path}")


# sqlite
def fastapi_sql_init():
    # create file and folder if not exist
    ensure_sqlite_db_exists(f"{SQLITE_DB_PATH}")

    # create tables if not exist
    sql_engine = create_engine(SQLITE_PATH)
    SQLModel.metadata.create_all(sql_engine)
    with Session(sql_engine) as sql_session:
        yield sql_session


def sql_init():
    # create file and folder if not exist
    ensure_sqlite_db_exists(f"{SQLITE_DB_PATH}")

    # create tables if not exist
    sql_engine = create_engine(SQLITE_PATH)
    SQLModel.metadata.create_all(sql_engine)
    sql_session = Session(sql_engine)
    return sql_session


# supabase
def supabase_init():
    # create tables if not exist, i uncommented it cause postgresql is giving error atm
    # sql_init()
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
    # initiate client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase