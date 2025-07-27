import datetime
import uuid

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from config import SUPABASE_URL, SUPABASE_KEY
from supabase import Client, create_client


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


if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Please set SUPABASE_URL and SUPABASE_KEY environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseDataManager(DataManagerInterface):
    def __init__(self, client: Client):
        if client is None:
            raise ValueError("Supabase client cannot be None")
        self.client = client

    def create_user(self, user: User):
        user_info = sterilize_for_json(user.model_dump(mode='python'))
        response = self.client.table('user').insert(user_info).execute()
        return response.data

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

    def create_chat(self, chat, user_id):
        pass

    def update_chat(self, chat_id):
        pass

    def delete_chat(self, chat_id):
        pass

user_example = User(name='user_four', email='user_four@example.com')
data_manager = SupabaseDataManager(supabase)
print(data_manager.create_user(user_example))
