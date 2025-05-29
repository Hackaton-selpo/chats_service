from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    role: str
    email: Optional[EmailStr]


class AIOutput(BaseModel):
    type: str
    body: str


class ImageOutput(AIOutput):
    title: str


class AudioOutput(ImageOutput):
    bg_image: str
