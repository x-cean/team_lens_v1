import datetime
from sqlmodel import Field, SQLModel


# models made using sqlmodel
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    password: str
    role: str = Field(default="user")
    organization: int | None = None
    workspace: int | None = None
    created_at: datetime = Field(default_factory=datetime.datetime.now)


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(default=f"Chat on {datetime.datetime.now().date()}")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.datetime.now)

