from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field


class ChatMessage(SQLModel, table = True):
    id : str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    message : str
    created_at : datetime = Field(default_factory=lambda: datetime.now())

class ChatMessagePayload(SQLModel):
    message : str

class ChatMessageListItem(SQLModel):
    message : str
    created_at : datetime = Field(default_factory=None)
