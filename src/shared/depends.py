from fastapi import HTTPException, Request, status


def get_access_token_from_headers(
    request: Request,
) -> str:
    headers = request.headers
    if headers.get("Authorization"):
        return headers.get("Authorization").split(" ")[-1]
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required"
    )
