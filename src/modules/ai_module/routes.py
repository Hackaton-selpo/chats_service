import asyncio
import base64
import logging

from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect
import base64

from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.ai_module.service import AIService
from src.modules.chats.services import ChatsService
from src.shared import schemas as shared_schemas, schemas
from src.shared.enums import MessageRole

"""
key = socket
value = {
tasks: []
}
"""
user_sockets = {}
router = APIRouter()


def decode_token(token: str) -> dict:
    encoded_string = token

    # Разделяем токен на три части
    header, payload, signature = encoded_string.split(".")

    # Функция для добавления padding и декодирования
    def decode_jwt_part(part):
        # Добавляем недостающие символы заполнения
        part += '=' * (-len(part) % 4)
        decoded = base64.urlsafe_b64decode(part).decode('utf-8')
        return decoded

    # Декодируем header и payload
    decoded_header = decode_jwt_part(header)
    decoded_payload = decode_jwt_part(payload)
    # print(111, decoded_header, decoded_payload)
    return decoded_payload.split(' ')[-1]


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
    # user: shared_schemas.User = get_current_user(token)
    payload_dict = eval(decode_token(token).replace('null', 'None'))
    payload_dict['id'] = payload_dict['sub']

    user = shared_schemas.User(**payload_dict)
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
                message_type='text'
            )
            tasks.clear()
            for done_task in asyncio.as_completed(pending_tasks):
                result = await done_task
                result: shared_schemas.AIOutput | shared_schemas.AudioOutput
                result = result.model_dump()
                # add additional info from db
                result["chat_id"] = chat_id
                ai_message_id = await ChatsService.insert_message(
                    chat_id,
                    result["body"],
                    role=MessageRole.ai,
                    letter_id=user_received_json.get("letter_id"),
                    message_type=result['type']
                )
                result["user_message_id"] = user_message_id
                result["ai_message_id"] = ai_message_id
                await websocket.send_json(result)
                # print(result)
    except WebSocketDisconnect:
        del user_sockets[websocket]
