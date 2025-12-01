from sqlmodel import Session, select, func
from app.logger import logger
from typing import Any

from .datamanager_interface import DataManagerInterface
from .models_trial_users import User, UsersPublic, Chat, ChatsPublic, Message, TrialChat, TrialMessage


class TrialSQLDataManager(DataManagerInterface):

    def __init__(self, *, session: Session):
        if session is None:
            logger.error("Attempt to initiate SQL DataManager without session")
            raise ValueError("Postgres session cannot be None")

        logger.info("Creating postgres session")
        self.session = session
        logger.info("Postgres session created successfully")

    def create_user(self, user_create: User) -> User:
        pass

    def get_all_users(self, skip: int = 0, limit: int = 100) -> Any:
        pass

    def get_user_by_id(self, user_id):
        pass

    def get_user_by_name(self, user_name):
        pass

    def get_user_by_email(self, user_email):
        pass

    def get_user_chats(self, user_id, skip: int = 0, limit: int = 100):
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

    def create_trial_chat(self):
        """
        Creates a trial chat for the trial user.
        """
        trial_chat = TrialChat()
        self.session.add(trial_chat)
        self.session.commit()
        self.session.refresh(trial_chat)
        return trial_chat

    def get_trial_chat_history_by_id(self, chat_id: int):
        """
        Retrieves the chat history for a given trial chat ID.
        """
        statement = select(TrialMessage).where(TrialMessage.chat_id == chat_id).order_by(TrialMessage.created_at)
        messages = self.session.exec(statement).all()
        if not messages:
            logger.warning(f"No messages found for chat ID {chat_id}")
            return None
        return messages[-10:]  # return the last 10 messages

    def get_trial_chat_by_id(self, chat_id):
        statement = select(TrialChat).where(TrialChat.id == chat_id)
        trial_chat = self.session.exec(statement).first()
        return trial_chat

    def get_trial_chat_history_by_id_2(self, chat_id: int):
        """
        Retrieves the chat history for a given trial chat ID.
        """
        trial_chat = self.get_trial_chat_by_id(chat_id)
        if not trial_chat:
            logger.warning(f"No trial chat found for chat ID {chat_id}")
            return None
        messages = trial_chat.messages
        if not messages:
            logger.warning(f"No messages found for chat ID {chat_id}")
            return None
        return messages[-10:]  # return the last 10 messages


    def save_trial_message(self, trial_message: TrialMessage) -> TrialMessage:
        """
        Creates a trial message for the trial chat.
        """
        self.session.add(trial_message)
        self.session.commit()
        self.session.refresh(trial_message)
        return trial_message
