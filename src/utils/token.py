from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

def get_token_from_header(request: Request) -> str:
    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing"
        )

    if not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )

    token = auth_header[7:].strip()  # len("Bearer ") == 7
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

    return token