from team_lens_v1.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_DB_PASSWORD, SUPABASE_URL_2
from supabase import Client, create_client
from sqlmodel import SQLModel, create_engine, Session, select

# sql
def postgresql_init():
    # create tables if not exist
    postgre_engine = create_engine(f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL_2}:5432/postgres")
    SQLModel.metadata.create_all(postgre_engine)
    return postgre_engine

# supabase
def supabase_init():
    # create tables if not exist
    postgresql_init()
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
    # initiate client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase