import datetime
import uuid

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class Chat(BaseModel):
    id: uuid.UUID
    title: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreatedMessageSchema(BaseModel):
    chat_id: uuid.UUID
    message_id: int
