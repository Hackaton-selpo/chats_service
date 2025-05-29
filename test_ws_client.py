import asyncio
import json

import websockets

# Замени на свой токен
JWT_TOKEN = """
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMiIsImVtYWlsIjpudWxsLCJyb2xlIjoiZ3Vlc3QiLCJleHAiOjE3NDg3NDMzODgsImlhdCI6MTc0ODUyNzM4OCwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiJ9.torlTbHzpplod7rsrTFjG2NKlR0vZ_76SxPffs4nmd3ajemPSEHc-Nr3uq81T-ue71hCBLo0nL6MY6mYM4JDc4Qzsk3qTBqW-wWW3RIAHblelRkdlfCZw5kWrsvL6sigEPAJteyzWYpKm2CuZOccOrGULloI2vIvF94E_eJWvnwcDx2lDthPs4aORXtcTInOPiPi-8EnjSEvtawRbDpJazmfqH5aDgiQYLBDhbbiTkUIlvLfV8EoPNoflZFQY3z7a1JOvQzDAvEGLvlc186EspVCDBsJe3i9zYkdEd6EMG8CX533splmaZiCxDvThQG5lf_lEd1tBCj5e4itz25Edg""".strip()
host = f"ws://127.0.0.1:8000/ws/{JWT_TOKEN}"
# host ="""
# wss://yamata-no-orochi.nktkln.com/chats/ws/
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NSIsImVtYWlsIjoiYWxleHJ1aV9ocG93QG1haWwucnUiLCJyb2xlIjoidXNlciIsImV4cCI6MTc0ODY2MzQ5NSwiaWF0IjoxNzQ4NDQ3NDk1LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIn0.LYaPfZeXLtxjrnff5C8GUYqdijvSVuN8K7htcxwk5Z7Llar-DxaP-F5svVb9E2xUt-ejxvm4ZYPMbEGJYodUd268uCFIUAWIx9GegPto4MZl2dBQyMd3c-bi4TMqnwFNIy1_xvd_W38pKHQha30AiGsxwjXiSXna2Mq-ycYuGa9oNzstJGffzDDSmlIo8oh8uSs2CVYy6DBaB9eW-nL--KCtuioH4aUw98UyNqFdG8YYvfZjovDcNKjZTkxxusd_koWiol3OKzF9mOmf-IRSyskSS64-TADTvHKM4eN6VfcpkyPskQVTdXmvQnnXR-s7VKbbjZP1zmIjOlEpnwzR2w
# """

async def connect_websocket():
    async with websockets.connect(
        host,
        # additional_headers={
        #     "chat_id": "4abb1f17-deb4-4dee-8cf9-3d04df173eac"
        # }
    ) as websocket:
        print("Подключено")

        # Первое сообщение — без chat_id
        first_message = {"body": "Создай историю о любви", "text": True}
        await websocket.send(json.dumps(first_message))
        print("Отправлено:", first_message)
        while True:
            response = await websocket.recv()

            data = json.loads(response)
            print("Получено:", data)

            # Если пришёл chat_id — можно отправить следующее сообщение
            if data.get("chat_id"):
                chat_id = data["chat_id"]
                second_message = {
                    "chat_id": chat_id,
                    "body": "поменяй имя на Лиза",
                    "text": True,
                }
                await websocket.send(json.dumps(second_message))
                print("Отправлено второе сообщение:", second_message)

            if data.get("body"):
                print("AI ОТВЕТ:", data["body"])
                break  # Выход после получения ответа
    async with websockets.connect(
        host,
        # additional_headers={
        #     "chat_id": "4abb1f17-deb4-4dee-8cf9-3d04df173eac"
        # }
    ) as websocket:
        print("Подключено")

        # Первое сообщение — без chat_id
        first_message = {"body": "Создай историю о любви", "image": True}
        await websocket.send(json.dumps(first_message))
        print("Отправлено:", first_message)
        while True:
            response = await websocket.recv()

            data = json.loads(response)
            print("Получено:", data)

            # Если пришёл chat_id — можно отправить следующее сообщение
            if data.get("chat_id"):
                chat_id = data["chat_id"]
                second_message = {
                    "chat_id": chat_id,
                    "body": "поменяй имя на Лиза",
                    "audio": True,
                }
                await websocket.send(json.dumps(second_message))
                print("Отправлено второе сообщение:", second_message)

            if data.get("body"):
                print("AI ОТВЕТ:", data["body"])
                break  # Выход после получения ответа


asyncio.run(connect_websocket())
