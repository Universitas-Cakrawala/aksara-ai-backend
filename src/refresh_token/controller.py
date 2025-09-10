from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict
from src.auth.handler import (
    refresh_access_token as external_refresh_access_token,
)  # Fungsi refresh token dari modul eksternal


class TokenHandler:

    class TokenResponse(BaseModel):
        access_token: str
        refresh_token: str

    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Dict[str, str]:
        # Panggil fungsi `refresh_access_token` dari modul `src.auth.handler`

        new_access_token = external_refresh_access_token(refresh_token)
        if new_access_token is None:
            raise HTTPException(
                status_code=401, detail="Invalid or expired refresh token"
            )

        # Return response in the required format
        return {
            "value": {"access_token": new_access_token, "refresh_token": refresh_token},
            "message": "Successfully refreshed access token!",
            "success_code": 200,
        }
