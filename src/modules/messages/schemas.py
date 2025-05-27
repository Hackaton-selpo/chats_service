import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from src.shared.enums import MessageRole


class Message(BaseModel):
    id: int
    chat_id: uuid.UUID
    body: str
    type: str
    role: MessageRole
    is_liked: Optional[bool] = None
    created_at: datetime.datetime
