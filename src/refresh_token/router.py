from fastapi import APIRouter, Header, HTTPException, Depends
from typing import Optional
from src.refresh_token.controller import (
    TokenHandler,
)  # Pastikan TokenHandler diimpor dengan benar
from src.auth.auth import RefreshTokenBearer

routerRefreshToken = APIRouter()
refresh_token_scheme = RefreshTokenBearer()


@routerRefreshToken.post("")
async def action(authorization: str = Depends(refresh_token_scheme)):
    # Mengambil token dengan menghilangkan kata `Bearer `
    refresh_token = authorization

    # Memanggil metode statis `refresh_access_token` pada `TokenHandler`
    response = TokenHandler.refresh_access_token(refresh_token)
    return response
