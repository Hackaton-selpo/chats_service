from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.modules.chats import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/login")


def get_user_from_token(
        # token: str = Depends(oauth2_scheme)
):
    # validate via grpc using auth service
    return schemas.User(
        id=1,
        name='danya'
    )
