import uuid

from datetime import datetime
from pydantic import EmailStr, model_validator
from sqlmodel import Field, Relationship, SQLModel


"""user chat msg models made using sqlmodel"""
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

    # uncomment if needed:
    # model_config = {
    #     "arbitrary_types_allowed": True
    # }

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
    # hashed_password: str | None = None # todo
    chats: list["Chat"] = Relationship(back_populates="owner", cascade_delete=True)


# properties to receive via API on update, all are optional
class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# message, shared properties
class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_system: bool = False
    sender_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    chat_id: int | None = Field(foreign_key="chat.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)

    # todo: only get sender_id when is_system is false?
    @model_validator(mode="after")
    def check_sender(self) -> "Message":
        if not self.is_system and not self.sender_id:
            raise ValueError("A non-system message must have a sender_id.")
        if self.is_system and self.sender_id:
            raise ValueError("A system message cannot have a sender_id.")
        return self

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
    id: int | None = Field(default=None, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="chats")


# properties to receive via API on update
class ChatPublic(ChatBase):
    id: int
    owner_id: uuid.UUID

class ChatsPublic(SQLModel):
    data: list[ChatPublic]
    count: int


"""resource workspace models made using sqlmodel"""
# resource file relevant models
class ResourceFile(SQLModel, table=True): #todo: for now keep it like this
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_path: str = Field(unique=True, min_length=3, max_length=255)
    name: str = Field(min_length=3, max_length=100)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    workspace_id: int | None = Field(foreign_key="workspace.id", nullable=True, ondelete="SET NULL")
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"ResourceFile(name: {self.name}, created_at: {self.created_at})"
    def __str__(self):
        return f"ResourceFile(name: {self.name}, created_at: {self.created_at})"

class ResourceFilePublic(SQLModel):
    id: uuid.UUID
    name: str
    created_at: datetime

class WorkspaceBase(SQLModel):
    name: str = Field(unique=True, min_length=3, max_length=30)
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"Workspace(name: {self.name}, created_at: {self.created_at})"

    def __str__(self):
        return f"Workspace(name: {self.name}, created_at: {self.created_at})"

class Workspace(WorkspaceBase, table=True): #todo:working on it
    id: int | None = Field(default=None, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    resource_files: list[ResourceFile] = Relationship(back_populates="workspace", cascade_delete=True)


"""trial chat msg models made using sqlmodel"""
# trial page models - no login, no history
class TrialMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_system: bool = False
    is_user: bool = True
    chat_id: int | None = Field(foreign_key="trialchat.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.now)
    chat: "TrialChat" = Relationship(back_populates="messages")

    # got this from copilot suggestion
    @model_validator(mode="after")
    def check_sender(self) -> "TrialMessage":
        if not self.is_system and not self.is_user:
            raise ValueError("Sender must be either system or user")
        if self.is_system and self.is_user:
            raise ValueError("Sender cannot be both system and user")
        return self

    def __repr__(self):
        return f"TrialMessage(created_at: {self.created_at})"

    def __str__(self):
        return f"TrialMessage(created_at: {self.created_at})"

class TrialChat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    messages: list[TrialMessage] = Relationship(back_populates="chat", cascade_delete=True)

    def __repr__(self):
        return f"TrialChat, created_at: {self.created_at})"

    def __str__(self):
        return f"TrialChat, created_at: {self.created_at})"
