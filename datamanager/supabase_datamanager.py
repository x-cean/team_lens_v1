import datetime
import uuid

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_DB_PASSWORD # add folder name when running from main script
from supabase import Client, create_client
from sqlmodel import SQLModel, create_engine


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

# create tables if not exist
engine = create_engine(f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.abmnqmqdnhoaqombygsy.supabase.co:5432/postgres")
SQLModel.metadata.create_all(engine)

# initiate client
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
        response = self.client.table("user").select("*").eq("id", user_id).execute()
        return User.model_validate(response.data[0])

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

data_manager = SupabaseDataManager(supabase)

# # create
# user_example = User(name='user_seven', email='user_seven@example.com')
# print(data_manager.create_user(user_example))

# get user by id
user_id = "90172268-181f-4495-b06e-b78cb64353a7"
print(data_manager.get_user_by_id(user_id))
