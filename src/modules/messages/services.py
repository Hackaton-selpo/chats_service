from sqlalchemy import update, and_
from src.database import async_session
from src.database.models import Message


class MessageService:
    @staticmethod
    async def like_dislike_message(
            is_liked: bool,
            chat_id: str,
            message_id: int,

    ):
        async with async_session() as session:
            async with session.begin():
                update_message_req = update(
                    Message
                ).where(and_(
                    Message.chat_id == chat_id,
                    Message.id == message_id
                )).values(
                    **{"is_liked": is_liked}
                )
                await session.execute(update_message_req)
