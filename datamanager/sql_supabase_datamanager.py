import datetime
import uuid

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from .sql_database_init import supabase_init, postgresql_init
from datetime import datetime
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
        return response.data # todo: maybe return user id?

    def get_all_users(self):
        pass

    def get_user_by_id(self, user_id):
        response = self.client.table("user").select("*").eq("id", user_id).execute()
        if response.data:
            user_data = response.data[0]
            user = User(**user_data)
            return user
        else:
            return None

    def get_user_by_name(self, user_name):
        response = self.client.table("user").select("*").eq("name", user_name).execute()
        if response.data:
            user_data = response.data[0]
            user = User(**user_data)
            return user
        else:
            return None

    def get_user_by_email(self, user_email):
        response = self.client.table("user").select("*").eq("email", user_email).execute()
        if response.data:
            user_data = response.data[0]
            # print(user_data)
            # print(user_data.get('items'))
            # user = User.model_validate(user_data)
            # print(type(user.created_at))
            if "created_at" in user_data and isinstance(user_data["created_at"], str):
                user_data["created_at"] = datetime.fromisoformat(user_data["created_at"])
            user = User(**user_data)
            ###todo: here validate always cause problem so i used **, but then datetime is str
            ###todo: weird, cause pydantic should handle it
            ###todo: from this point it appears that supabase lib is not the best fit for python
            ###todo: will use sqlmodel that allows working with python object directly
            return user
        else:
            return None

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
        msg_info = sterilize_for_json(msg.model_dump(mode='python'))
        response = self.client.table('message').insert(msg_info).execute()
        return response.data # todo: check and decide what to return

# # start database
# supabase_client = supabase_init()
# data_manager = SupabaseDataManager(supabase_client)

# # create
# user_example = User(name='user_six', email='user_six@example.com')
# print(data_manager.create_user(user_example))

# # get user by id
# a_user_id = "90172268-181f-4495-b06e-b78cb64353a7"
# print(data_manager.get_user_by_id(a_user_id))

# # get user by name
# a_user_name = "user_six"
# print(data_manager.get_user_by_name(a_user_name))

# # get user by email
# a_user_email = "user_six@example.com"
# print(data_manager.get_user_by_email(a_user_email))

# create msg
# a_msg = Message(text="Hello, what can I help you", is_system=True, chat_id=1)