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


