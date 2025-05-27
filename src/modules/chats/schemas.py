import datetime
import uuid

from pydantic import BaseModel


class Chat(BaseModel):
    id: uuid.UUID
    title: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
