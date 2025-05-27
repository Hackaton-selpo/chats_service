from sqlalchemy import and_, update

from src.database import async_session
from src.database.models import Chat, Message


class MessageService:
    @staticmethod
    async def like_dislike_message(
        is_liked: bool,
        chat_id: str,
        message_id: int,
    ):
        async with async_session() as session, session.begin():
            update_message_req = (
                update(Message)
                .where(and_(Message.chat_id == chat_id, Message.id == message_id))
                .values(**{"is_liked": is_liked})
            )
            await session.execute(update_message_req)

    @staticmethod
    async def publish_message(message_id: int, user_id: int):
        async with async_session() as session, session.begin():
            chunked_message = await session.execute(
                update(Message)
                .where(
                    and_(
                        Message.chat_id == Chat.id,
                        Chat.user_id == user_id,
                        Message.id == message_id,
                    )
                )
                .values(
                    **{"is_published": True},
                )
                .returning(Message.id)
            )
            return chunked_message.scalar()
