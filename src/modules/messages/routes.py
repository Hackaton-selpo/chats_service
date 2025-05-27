from fastapi import APIRouter, Depends

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.messages.services import MessageService
from src.shared import schemas as shared_schemas

router = APIRouter()


@router.patch(
    "/{chat_id}/{message_id}",
)
async def like_dislike_message(is_liked: bool, chat_id: str, message_id: int):
    await MessageService.like_dislike_message(is_liked, chat_id, message_id)


# @router.get(
#     "/{message_id}",
#     response_model=schemas.Message
# )
# async def get_message(message_id: int):
#     """
#     get message from db, check field is published
#     :param message_id:
#     :return:
#     """
#     message: Optional[Message]
#     if not (message := await MessageService.get_message(message_id)):
#         raise HTTPException(status_code=403, detail="Message not found or not published")
#     message.type = get_message_type(message.body)
#     return message


@router.patch("/{message_id}")
async def publish_message(
    message_id: int, user: shared_schemas.User = Depends(get_current_user)
):
    await MessageService.publish_message(message_id, user.id)
