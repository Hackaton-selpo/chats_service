import asyncio
import json

import websockets

# Замени на свой токен
JWT_TOKEN = """
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImVtYWlsIjoiZ3Vza2lyMjYwNkBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTc0ODU1NTExNywiaWF0IjoxNzQ4MzM5MTE3LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIn0.hB19ailT-qUFXFmM6Q2-wJR6ZAGO4KBocvTKeDYbLMsTMU7-hp4B57XoF5V7WIHf1dGI7mWuh11qu9NYoOcXuB6PIsf11oxNQ7cHkkTxBNgho9sH6vd8GENHf7WVvfV34FrQCzHqByFjOHPcmZKnZHQcb9GRw4CshRQb0bqofIqPdb-ND-q-5-irJ-xC3ko-G629XOwqBZzuvbmS-9A-FVWwjHfyRiJ0TYhTZwB_Ip2TMVpCMNe54Ztk4JmM89RnkSjxlPxKyoyFYNfbJQ9YubYBQHCPzOnyDN65GtZToeJDMo85LioQ_2TINn6_4ldqWuXMXufED7TqTi8-qlD0Tw
""".strip()
host = f"ws://127.0.0.1:8000/ws/{JWT_TOKEN}"


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
