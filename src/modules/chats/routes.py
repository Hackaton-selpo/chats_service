from fastapi import APIRouter, Depends

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.chats.schemas import Chat
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
