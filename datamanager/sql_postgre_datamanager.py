import datetime
import uuid

from sqlmodel import SQLModel, create_engine, Session, select, func
from team_lens_v1.logger import logger
from typing import Any

from .datamanager_interface import DataManagerInterface
from .models import User, UsersPublic, Chat, ChatsPublic, Message
from .sql_database_init import supabase_init, postgresql_init


class PostgresDataManager(DataManagerInterface):

    def __init__(self, *, session: Session):
        if session is None:
            logger.error("Attempt to initiate PostgresDataManager without session")
            raise ValueError("Postgres session cannot be None")

        logger.info("Creating postgres session")
        self.session = session
        logger.info("Postgres session created successfully")

    def create_user(self, user_create: User) -> User:
        self.session.add(user_create)
        self.session.commit()
        logger.info(f"User {user_create.name} created successfully with ID {user_create.id}")

        self.session.refresh(user_create)
        return user_create

    def get_all_users(self, skip: int = 0, limit: int = 100) -> Any:
        count_statement = select(func.count()).select_from(User)
        count = self.session.exec(count_statement).one()

        statement = select(User).offset(skip).limit(limit)
        users = self.session.exec(statement).all()

        return UsersPublic(data=users, count=count)

    def get_user_by_id(self, user_id):
        statement = select(User).where(User.id == user_id)
        session_user = self.session.exec(statement).first()
        return session_user

    def get_user_by_name(self, user_name):
        statement = select(User).where(User.name == user_name)
        session_user = self.session.exec(statement).first()
        return session_user

    def get_user_by_email(self, user_email):
        statement = select(User).where(User.email == user_email)
        session_user = self.session.exec(statement).first()
        return session_user

    def get_user_chats(self, user_id, skip: int = 0, limit: int = 100):
        session_user = self.get_user_by_id(user_id)
        if not session_user:
            logger.error(f"User with ID {user_id} not found")
            return None

        count_statement = (select(func.count()).select_from(Chat)
                           .where(Chat.owner_id == user_id))
        count = self.session.exec(count_statement).one()

        statement = select(Chat).where(Chat.owner_id == user_id).offset(skip).limit(limit)
        user_chats = self.session.exec(statement).all()

        return ChatsPublic(data=user_chats, count=count)

    def get_chat_by_id(self, chat_id):
        pass

    def update_user(self, user_id):
        pass

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            logger.error(f"User with ID {user_id} not found")
            return Message(message="User not found")
        self.session.delete(user)
        self.session.commit()
        return Message(message="User deleted successfully"), "User deleted successfully"
        # todo: what to return here?

    def create_chat(self, chat: Chat, user_id):
        pass

    def update_chat(self, chat_id):
        pass

    def delete_chat(self, chat_id):
        pass

    def create_message(self, msg: Message):
        pass


