from typing import Optional

from fastapi import APIRouter, Depends

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.chats.schemas import Chat, CreatedMessageSchema
from src.modules.chats.services import ChatsService
from src.modules.messages.schemas import Message
from src.shared import schemas as shared_schemas

router = APIRouter()


@router.get("/", response_model=list[Chat])
async def get_user_chats(user: shared_schemas.User = Depends(get_current_user)):
    return await ChatsService.get_user_chats(user.id)


@router.get("/{chat_id}/messages", response_model=list[Message])
async def get_chats_messages(chat_id: str):
    return await ChatsService.get_chat_messages(chat_id)


@router.post("/", response_model=CreatedMessageSchema)
async def send_message_to_ai(
    user_prompt: str,
    chat_id: Optional[str] = None,
    user: shared_schemas.User = Depends(get_current_user),
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
