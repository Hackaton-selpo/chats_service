from fastapi import APIRouter

from src.modules.messages.services import MessageService

router = APIRouter()


@router.patch(
    "/{chat_id}/{message_id}",
)
async def like_dislike_message(is_liked: bool, chat_id: str, message_id: int):
    await MessageService.like_dislike_message(is_liked, chat_id, message_id)
