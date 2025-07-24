import datetime
import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


"""models made using sqlmodel"""
# user: shared properties
class UserBase(SQLModel):
    name: str
    full_name: str
    password: EmailStr
    role: str = Field(default="user")
    is_active: bool = True
    is_superuser: bool = False
    organization: int | None = None
    workspace: int | None = None
    created_at: datetime = Field(default_factory=datetime.datetime.now)


# user creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# todo: user crud


# user database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str # todo
    items: list["Chat"] = Relationship(back_populates="owner", cascade_delete=True)





class ChatBase(SQLModel):
    title: str = Field(default=f"Chat on {datetime.datetime.now().date()}")
    created_at: datetime = Field(default_factory=datetime.datetime.now)
    history: list[str] | None = None


# todo: crud


# chat database model, database table inferred from class name
class Chat(ChatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")

