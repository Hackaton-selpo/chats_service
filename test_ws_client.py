import asyncio
import json

import websockets

# Замени на свой токен
JWT_TOKEN = """
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImVtYWlsIjoiZ3Vza2lyMjYwNkBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTc0ODI2ODk0NywiaWF0IjoxNzQ4MjY4NjQ3LCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIn0.Fipp6Me8ydQ79TtcHZQ7Ls83yBdBCJ8bL8u2cfB17ISGmXHD-7QLBtrD95A08J3PneN4Jp8RGKmnIkr1v2pmE-RQl7_xYIuO7Av57bBlEQiaec1qoAgZa3lKwjw7Qiz57jhHoItuaRyCNBLbwjoQRbiVM1ocorAyoBMxWvWmVnxDdBKI2wTgCUdWX6DEaN_lPv6ATY6DauXlrHIOTs5mcqmn_883s-Dzav6sm_hkZ3y2BQsVPZacUQHOa13G8iJTcVaZY43XWNqRMVKySgmnsL-Z_lOhfLxLsoKQE_T2fpTQk_3w_c299WlP21_ZQ9npihkzeWfS1CwKGjLcw7wg4Q
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
        first_message = {"text": "Создай историю о любви"}
        await websocket.send(json.dumps(first_message))
        print("Отправлено:", first_message)

        while True:
            response = await websocket.recv()

            data = json.loads(response)
            print("Получено:", data)

            # Если пришёл chat_id — можно отправить следующее сообщение
            if "chat_id" in data:
                pass
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
