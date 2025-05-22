from fastapi import APIRouter, Depends

from src.grpc_token_checker.token_validator import get_current_user
from src.modules.chats.routes import router as chats_router
from src.modules.messages.routes import router as messages_router

main_router = APIRouter()
main_router.include_router(chats_router, prefix="/chats", tags=["chats"])
main_router.include_router(messages_router, prefix="/messages", tags=["messages"])


@main_router.get("/ping")
async def ping():
    return {"ping": "pong"}


@main_router.get("/")
async def root(
        _=Depends(get_current_user)
):
    pass
