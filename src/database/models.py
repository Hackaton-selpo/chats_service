import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.shared.enums import MessageRole


class MessageType(Base):
    __tablename__ = "messages_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    messages: Mapped[list["Message"]] = relationship(
        back_populates="message_type", order_by="Message.created_at"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_type_id: Mapped[int] = mapped_column(ForeignKey("messages_types.id"))
    body: Mapped[str] = mapped_column()
    is_liked: Mapped[Optional[bool]] = mapped_column()
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    is_published: Mapped[bool] = mapped_column(
        server_default="False", default=False, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))

    # Relationships
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    message_type: Mapped["MessageType"] = relationship(back_populates="messages")
    letter_id: Mapped[str] = mapped_column(nullable=True)


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat", order_by="Message.created_at"
    )