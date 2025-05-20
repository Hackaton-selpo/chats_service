from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from src.modules.chats import schemas
from src.modules.chats.services import ChatsService

from src.modules.chats.depends import get_user_from_token
from src.modules.messages.services import MessageService

router = APIRouter()


@router.patch(
    '/{chat_id}/{message_id}',
)
async def like_dislike_message(
        is_liked: bool,
        chat_id: str,
        message_id: int
):
    await MessageService.like_dislike_message(is_liked, chat_id, message_id)
