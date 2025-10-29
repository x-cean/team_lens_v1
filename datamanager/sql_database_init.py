from requests import session

from team_lens_v1.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_DB_PASSWORD, SUPABASE_URL_2, SUPABASE_DB_STRING
from supabase import Client, create_client
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import Depends
from typing import Annotated

SESSION_POOLER_SITE = f"postgresql+psycopg2://postgres.{SUPABASE_DB_STRING}:{SUPABASE_DB_PASSWORD}@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
DIRECT_CONNECTION_SITE = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL_2}:5432/postgres"


# sql
def fastapi_postgresql_init():
    # create tables if not exist
    postgres_engine = create_engine(DIRECT_CONNECTION_SITE)
    SQLModel.metadata.create_all(postgres_engine)
    with Session(postgres_engine) as postgres_session:
        yield postgres_session

def postgresql_init():
    postgres_engine = create_engine(DIRECT_CONNECTION_SITE)
    SQLModel.metadata.create_all(postgres_engine)
    postgres_session = Session(postgres_engine)
    return postgres_session

# supabase
def supabase_init():
    # create tables if not exist, i uncommented it cause postgresql is giving error atm
    # postgresql_init()
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
    # initiate client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase