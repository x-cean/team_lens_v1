from datetime import datetime
from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel


"""models for the trial page, made using sqlmodel"""
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
