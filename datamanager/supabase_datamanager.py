import datetime
import uuid

from .datamanager_interface import DataManagerInterface
from .models import User, Chat, Message
from team_lens_v1.config import SUPABASE_URL, SUPABASE_KEY
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

def create_user(user: User) -> User:
    user_entry = supabase.table('user').insert(user.model_dump(mode='python')).execute()
    return user

user_one = User(name='user_one', email='user_one@example.com')
create_user(user_one)

