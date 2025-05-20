import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.shared.enums import MessageRole


class Message(Base):
    __tablename__ = "messages"

    body: Mapped[str] = mapped_column()
    is_liked: Mapped[Optional[bool]] = mapped_column()
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    chat: Mapped["Chat"] = relationship(
        back_populates="messages"
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(),
        server_default=func.now()
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        order_by="Message.created_at"
    )
