from fastapi import APIRouter

from src.modules.ai_module.routes import router as ai_router
from src.modules.chats.routes import router as chats_router
from src.modules.messages.routes import router as messages_router

main_router = APIRouter()
main_router.include_router(chats_router, prefix="/chats", tags=["chats"])
main_router.include_router(messages_router, prefix="/messages", tags=["messages"])
main_router.include_router(ai_router, tags=["AI"])


@main_router.get("/ping")
async def ping():
    return {"ping": "pong"}
