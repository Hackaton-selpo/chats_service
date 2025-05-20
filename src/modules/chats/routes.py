from typing import Optional

from fastapi import APIRouter, Depends

from src.modules.chats import schemas
from src.modules.chats.depends import get_user_from_token
from src.modules.chats.schemas import Chat, CreatedMessageSchema
from src.modules.chats.services import ChatsService
from src.modules.messages.schemas import Message

router = APIRouter()


@router.get("/", response_model=list[Chat])
async def get_user_chats(user: schemas.User = Depends(get_user_from_token)):
    return await ChatsService.get_user_chats(user.id)


@router.get("/{chat_id}/messages", response_model=list[Message])
async def get_chats_messages(chat_id: str):
    return await ChatsService.get_chat_messages(chat_id)


@router.post("/", response_model=CreatedMessageSchema)
async def send_message_to_ai(
    user_prompt: str,
    chat_id: Optional[str] = None,
    user: schemas.User = Depends(get_user_from_token),
):
    if not chat_id:
        # create chat
        chat_id = await ChatsService.create_chat(
            user_id=user.id,
            user_prompt=user_prompt,
        )

    return {
        "chat_id": chat_id,
        "message_id": await ChatsService.insert_message(chat_id, user_prompt),
    }
