from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    role: str
    email: EmailStr
