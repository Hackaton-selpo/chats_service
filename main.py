import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

from src.database import init_models
from src.grpc_token_checker.token_validator_depends import get_current_user
from src.modules.chats.services import ChatsService
from src.routes import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await init_models()
    yield


app = FastAPI(lifespan=lifespan, root_path="/chats")
app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
)

from src.shared import schemas as shared_schemas


@app.get("/test")
def tes():
    return None


@app.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
):
    await websocket.accept()
    user: shared_schemas.User = get_current_user(token)

    while True:
        if websocket.headers.get("chat_id") is None:
            # create chat
            chat_id = await ChatsService.create_chat(
                user_id=user.id,
                user_prompt="New chat",
            )
            await websocket.send_json({"chat_id": chat_id})
        user_prompt = await websocket.receive_json()
        async with httpx.AsyncClient(timeout=200) as client:
            ai_answer = await client.get(
                "http://localhost:8052/get_llm_answer",
                params={
                    "prompt": user_prompt["text"],
                },
            )
            ai_text = ai_answer.json()["ai_answer"]
            await websocket.send_json({"ai_answer": ai_text})
