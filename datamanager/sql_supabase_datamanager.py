import datetime
import uuid

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from .sql_database_init import supabase_init, postgresql_init
from sqlmodel import SQLModel, create_engine, Session, select
from supabase import Client


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
        response = self.client.table("user").select("*").eq("id", user_id).execute()
        print(response.data[0])
        print(User.model_fields)
        user_data = response.data[0]
        user_data['items'] = []
        print(user_data.get('items'))
        print("not found")
        return User.model_validate(user_data)

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

supabase_client = supabase_init()
data_manager = SupabaseDataManager(supabase_client)

# # create
# user_example = User(name='user_six', email='user_six@example.com')
# print(data_manager.create_user(user_example))

# get user by id
user_id = "90172268-181f-4495-b06e-b78cb64353a7"
print(data_manager.get_user_by_id(user_id))
