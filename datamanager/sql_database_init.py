import os

from requests import session

from team_lens_v1.logger import logger
from team_lens_v1.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_DB_PASSWORD, SUPABASE_URL_2, SUPABASE_DB_STRING
from supabase import Client, create_client
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import Depends
from typing import Annotated
from pathlib import Path


SESSION_POOLER_SITE = (f"postgresql+psycopg2://postgres.{SUPABASE_DB_STRING}:{SUPABASE_DB_PASSWORD}"
                       f"@aws-1-eu-north-1.pooler.supabase.com:5432/postgres")
DIRECT_CONNECTION_SITE = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL_2}:5432/postgres"
SQLITE_PATH = "sqlite:///../../team_lens.db"


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


# sql
def fastapi_sql_init():
    # create tables if not exist
    sql_engine = create_engine(SQLITE_PATH)
    SQLModel.metadata.create_all(sql_engine)
    with Session(sql_engine) as sql_session:
        yield sql_session


def sql_init():
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