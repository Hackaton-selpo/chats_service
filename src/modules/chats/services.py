import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import insert, select

from src.database import async_session
from src.database.models import Chat, Message
from src.shared.enums import MessageRole


class ChatsService:
    @staticmethod
    async def get_user_chats(user_id: int):
        async with async_session() as session:
            chats_req = select(Chat).where(Chat.user_id == user_id)
            chunked_chats = await session.execute(chats_req)
            return chunked_chats.scalars().all()

    @staticmethod
    async def get_chat_messages(chat_id: str):
        async with async_session() as session:
            messages_req = (
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc())
            )
            chunked_messages = await session.execute(messages_req)
            return chunked_messages.scalars().all()

    @staticmethod
    async def insert_message(chat_id: int, user_prompt: str) -> int:
        async with async_session() as session, session.begin():
            try:
                insert_message_req = (
                    insert(Message)
                    .values(chat_id=chat_id, body=user_prompt, role=MessageRole.user)
                    .returning(Message.id)
                )
                inserted_messaged_id_chunked = await session.execute(insert_message_req)
                return inserted_messaged_id_chunked.scalar()
            except sqlalchemy.exc.DBAPIError as e:
                raise HTTPException(
                    status_code=400, detail="Chat creation failed."
                ) from e

    @staticmethod
    async def create_chat(user_prompt: str, user_id: int):
        async with async_session() as session, session.begin():
            insert_chat_req = (
                insert(Chat)
                .values(title=user_prompt[:50], user_id=user_id)
                .returning(Chat.id)
            )
            chat_id_chunked = await session.execute(insert_chat_req)
            return chat_id_chunked.scalar()
