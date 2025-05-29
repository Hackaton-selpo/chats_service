from typing import Optional

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import insert, select

from src.database import async_session
from src.database.models import Chat, Message
from src.shared.enums import MessageRole
from src.shared.funcs import get_message_type


class ChatsService:
    @staticmethod
    async def get_user_chats(user_id: int):
        async with async_session() as session:
            chats_req = select(Chat).where(Chat.user_id == user_id)
            chunked_chats = await session.execute(chats_req)
            return chunked_chats.scalars().all()

    @staticmethod
    async def get_chat_messages(chat_id: str) -> list[dict]:
        """
        also add message type
        :param chat_id:
        :return: list with dicts with consisting of Messages with a field <type> (audio/image/text)
        """
        async with async_session() as session:
            messages_req = (
                select(Message)
                .where(Message.chat_id == chat_id)
                .order_by(Message.created_at.desc())
            )
            chunked_messages = await session.execute(messages_req)
        messages = chunked_messages.scalars().all()
        result_messages = []
        for message in messages:
            message.type = get_message_type(message["body"])
            result_messages.append(message)
        return result_messages

    @staticmethod
    async def insert_message(
            chat_id: int,
            user_prompt: str,
            role: MessageRole = MessageRole.user,
            letter_id: Optional[str] = None,
    ) -> int:
        async with async_session() as session, session.begin():
            try:
                insert_message_req = (
                    insert(Message)
                    .values(chat_id=chat_id, body=user_prompt, role=role, letter_id=letter_id)
                    .returning(Message.id)
                )
                inserted_messaged_id_chunked = await session.execute(insert_message_req)
                return inserted_messaged_id_chunked.scalar()
            except sqlalchemy.exc.DBAPIError as e:
                raise HTTPException(
                    status_code=400, detail="Message creating failed"
                ) from e

    @staticmethod
    async def create_chat(user_prompt: str, user_id: int) -> str:
        async with async_session() as session, session.begin():
            insert_chat_req = (
                insert(Chat)
                .values(title=user_prompt[:50], user_id=user_id)
                .returning(Chat.id)
            )
            chat_id_chunked = await session.execute(insert_chat_req)
            return str(chat_id_chunked.scalar())
