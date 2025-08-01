import datetime
import uuid

from sqlmodel import SQLModel, create_engine, Session, select
from team_lens_v1.logger import logger

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from .sql_database_init import supabase_init, postgresql_init

def sterilize_for_json(data: dict) -> dict:
    result = {}
    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            result[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            result[key] = str(value)
        else:
            result[key] = value
    return result


class PostgresDataManager(DataManagerInterface):
    def __init__(self, *, session: Session):
        if session is None:
            logger.error("Attempt to initiate PostgresDataManager without session")
            raise ValueError("Postgres session cannot be None")
        logger.info("Creating postgres session")
        self.session = session
        logger.info("Postgres session created successfully")

    def create_user(self, user_create: User):
        self.session.add(user_create)
        self.session.commit()
        self.session.refresh(user_create)
        return user_create

    def get_all_users(self):
        pass

    def get_user_by_id(self, user_id):
        pass

    def get_user_by_name(self, user_name):
        pass

    def get_user_by_email(self, user_email):
        pass

    def get_user_chats(self, user_id):
        pass

    def get_chat_by_id(self, chat_id):
        pass

    def update_user(self, user_id):
        pass

    def delete_user(self, user_id):
        pass

    def create_chat(self, chat: Chat, user_id):
        pass

    def update_chat(self, chat_id):
        pass

    def delete_chat(self, chat_id):
        pass

    def create_message(self, msg: Message):
        pass


