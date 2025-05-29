import asyncio
import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.ai_module.service import AIService
from src.modules.chats.services import ChatsService
from src.shared import schemas as shared_schemas
from src.shared.enums import MessageRole

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
    chat_id: Optional[uuid] (from headers)
    text: str (user_prompt)
    audio: Optional[bool] (generate audio?)
    image: Optional[bool] (generate image?)
    audio: Optional[bool] (generate audio?)
    letter_id : Optional[str] (letter reference id from getter service)
    }

    out: {
    chat_id: uuid
    type: str (audio,text,image)
    body: str (image url, audio url, text)
    }
    :param websocket:
    :param token:
    :return:
    """
    await websocket.accept()
    user: shared_schemas.User = get_current_user(token)
    user_sockets[websocket] = {"tasks": []}
    try:
        while True:
            if websocket.headers.get("chat_id") is None:
                # create chat
                chat_id = await ChatsService.create_chat(
                    user_id=user.id,
                    user_prompt="New chat",
                )
            else:
                chat_id = websocket.headers.get("chat_id")
            user_received_json = await websocket.receive_json()

            tasks = user_sockets[websocket]["tasks"]
            if user_received_json.get("text"):
                tasks.append(
                    AIService().generate_ai_text_answer(
                        user_received_json["body"], user_received_json.get("letter_id")
                    )
                )
            if user_received_json.get("image"):
                tasks.append(
                    AIService().generate_ai_image_answer(
                        user_received_json["body"], user_received_json.get("letter_id")
                    )
                )
            if user_received_json.get("audio"):
                tasks.append(
                    AIService().generate_ai_audio_answer(
                        user_received_json["body"],
                        user_received_json.get("letter_id"),
                        user_received_json.get("audio_text")

                    )
                )

            pending_tasks = [asyncio.create_task(t) for t in tasks]
            user_message_id = await ChatsService.insert_message(
                chat_id, user_received_json["body"], role=MessageRole.user,
                letter_id=user_received_json.get("letter_id"),
            )
            tasks.clear()
            for done_task in asyncio.as_completed(pending_tasks):
                result = await done_task
                result: shared_schemas.AIOutput | shared_schemas.AudioOutput
                result = result.model_dump()
                # add additional info from db
                result["chat_id"] = chat_id
                ai_message_id = await ChatsService.insert_message(
                    chat_id, result["body"], role=MessageRole.ai,
                    letter_id=user_received_json.get("letter_id"),
                )
                result["user_message_id"] = user_message_id
                result["ai_message_id"] = ai_message_id
                await websocket.send_json(result)
                # print(result)
    except WebSocketDisconnect:
        del user_sockets[websocket]
