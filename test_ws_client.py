import asyncio
import json

import websockets

# Замени на свой токен
JWT_TOKEN = """
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImVtYWlsIjoiZ3Vza2lyMjYwNkBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTc0ODMzODI3MywiaWF0IjoxNzQ4MzM3OTczLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIn0.kXsNwDCiezF8jw1Gc-qYzhMsBHA4zzt2Y-nu7z5FX7aO1F9J3431pXQOLuWdbejImOS-jcxv03d-B2n7FOr6QQlrnBxo78n_I5jABXbRmBDeqEBRhErIhK96BIXD_DGI4SqrGf-3Kgm5SF0t2Gk8BpjpATBTyFj-BKQ58PnpzQavlKJTk1_fjAi6mHw5dB9-yWLTESodEPRGRQDVSMVfSL474L5nE1FJ02TBPcii1xs_58hUUCFZud_wPmhYXrAwQmx15TjUa1djV6EjfE0lXgXD5SopN4Q2-Rl48RQccHHXGAV5RrpOr4qkM2684ynWn1nUsqfdJE4uqaMG91O0ZQ
""".strip()


async def connect_websocket():
    uri = f"ws://127.0.0.1:8000/ws/{JWT_TOKEN}"  # если токен принимается через query-param

    async with websockets.connect(
        uri,
        # additional_headers={
        #     "chat_id" : "chat_id"
        # }
    ) as websocket:
        print("Подключено")

        # Первое сообщение — без chat_id
        first_message = {"body": "Создай историю о любви", "text": True}
        await websocket.send(json.dumps(first_message))
        print("Отправлено:", first_message)
        chat_id = ""
        while True:
            response = await websocket.recv()

            data = json.loads(response)
            print("Получено:", data)

            # Если пришёл chat_id — можно отправить следующее сообщение
            if data.get("chat_id"):
                chat_id = data["chat_id"]
                # second_message = {
                #     "chat_id": data["chat_id"],
                #     "text": "Расскажи мне о квантовых вычислениях"
                # }
                # await websocket.send(json.dumps(second_message))
                # print("Отправлено второе сообщение:", second_message)

            if "ai_answer" in data:
                print("AI ОТВЕТ:", data["ai_answer"])
                break  # Выход после получения ответа


asyncio.run(connect_websocket())
