# chat_service_client.py
import grpc
from fastapi import Depends, HTTPException, status

from src.grpc_token_checker import auth_service_pb2, auth_service_pb2_grpc
from src.shared import schemas as shares_schemas
from src.shared.depends import get_access_token_from_headers


def get_auth_service_stub():
    channel = grpc.insecure_channel("localhost:50051")
    return auth_service_pb2_grpc.AuthServiceStub(channel)


def get_current_user(token: str = Depends(get_access_token_from_headers)):
    stub = get_auth_service_stub()
    try:
        response = stub.CheckToken(auth_service_pb2.TokenRequest(token=token))
        if not response.valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {response.error}",
            )
        response.claims["id"] = response.claims["sub"]
        return shares_schemas.User(**response.claims)
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Auth service unavailable: {e}",
        ) from e
