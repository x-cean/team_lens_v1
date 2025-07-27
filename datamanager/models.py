import uuid

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


"""models made using sqlmodel"""
# user, shared properties
class UserBase(SQLModel):
    name: str = Field(unique=True, min_length=3, max_length=30)
    full_name: str | None = None
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    organization: int | None = None
    workspace: int | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "arbitrary_types_allowed": True
    }

    def __repr__(self):
        return f"User(name: {self.name}, created_at: {self.created_at})"

    def __str__(self):
        return f"User(name: {self.name}, created_at: {self.created_at})"


# user creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# todo: user crud


# user database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # id: int = Field(default=None, primary_key=True)
    # hashed_password: str | None = None # todo
    items: list["Chat"] = Relationship(back_populates="owner", cascade_delete=True)


# message, shared properties
class Message(SQLModel):
    text: str
    # created_at: datetime = Field(default_factory=datetime.now)
    is_system: bool = False
    sender_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)

    # todo: only get sender_id when is_system is false?
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_sender_id

    @classmethod
    def validate_sender_id(cls, values):
        is_system = values.get("is_system")
        sender_id = values.get("sender_id")
        if not is_system and sender_id is None:
            raise ValueError("sender_id is required when is_system is False")
        elif is_system and sender_id is not None:
            raise ValueError("sender_id is not required when is_system is True")
        return values

    def __repr__(self):
        return f"Message, created_at: {self.created_at})"

    def __str__(self):
        return f"Message, created_at: {self.created_at})"


# chat, shared properties
class ChatBase(SQLModel):
    title: str = Field(default=f"Chat on {datetime.now().date()}", min_length=10, max_length=255)
    # created_at: datetime = Field(default_factory=datetime.now)
    history: str | None = None # todo: think about what to put here

    def __repr__(self):
        return f"Chat, title: {self.title}, created_at: {self.created_at})"

    def __str__(self):
        return f"Chat, title: {self.title}, created_at: {self.created_at})"

# todo: crud


# chat database model, database table inferred from class name
class Chat(ChatBase, table=True):
    # id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: int | None = Field(default=None, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")



