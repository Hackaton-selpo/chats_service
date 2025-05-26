import asyncio

from fastapi import APIRouter
from starlette.websockets import WebSocket

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.ai_module.service import AIService
from src.modules.chats.services import ChatsService
from src.shared import schemas as shared_schemas

"""
key = socket
value = {
tasks: []
}
"""
user_sockets = {}
router = APIRouter()


@router.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
):
    """
    при первом запросе проверяет токен,
    создает пустой список тасок для асинхронного запуска задач генерации
    создает чат в бд
    Обмен происходит по контракту:
    in: {
    chat_id:uuid (from headers)
    text:str (user_prompt)
    audio: Optional[bool] (generate audio?)
    image: Optional[bool] (generate image?)
    audio: Optional[bool] (generate audio?)
    letter_id : Optional[int] (letter reference id in db)
    }

    :param websocket:
    :param token:
    :return:
    """
    await websocket.accept()
    user: shared_schemas.User = get_current_user(token)
    user_sockets[websocket] = {"tasks": []}
    while True:
        if websocket.headers.get("chat_id") is None:
            # create chat
            chat_id = await ChatsService.create_chat(
                user_id=user.id,
                user_prompt="New chat",
            )
            await websocket.send_json({"chat_id": chat_id})
        user_prompt = await websocket.receive_json()

        tasks = user_sockets[websocket]["tasks"]
        if user_prompt.get("audio"):
            tasks.append(
                AIService().generate_ai_text_answer(
                    user_prompt["text"], user_prompt.get("letter_id")
                )
            )
        if user_prompt.get("image"):
            tasks.append(
                AIService().generate_ai_image_answer(
                    user_prompt["text"], user_prompt.get("letter_id")
                )
            )
        if user_prompt.get("text"):
            tasks.append(
                AIService().generate_ai_audio_answer(
                    user_prompt["text"], user_prompt.get("letter_id")
                )
            )

        pending_tasks = [asyncio.create_task(t) for t in tasks]
        tasks.clear()
        for done_task in asyncio.as_completed(pending_tasks):
            result = await done_task
            result: shared_schemas.AIOutput
            await websocket.send_json(result.model_dump())
            # print(result)
