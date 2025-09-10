from fastapi import APIRouter, Depends, Header
from src.user.controller import UserController
from src.auth.auth import JWTBearer, OptionalJWTBearer
from typing import Optional
from src.config.postgres import get_db
from sqlalchemy.orm import Session
from src.auth.handler import decodeJWT
from src.user.schemas import (
    UserCreate,
    UserUpdate,
    UserLogin,
    Verify2FA,
    UserGenerateOtpParams,
    PasswordUpdate,
    PasswordUpdateByUsername,
    UserSearchParams,
)
from src.utils.pagination import PageParams


routerUser = APIRouter()


@routerUser.post("/register")
async def action(
    request: UserCreate,
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Depends(OptionalJWTBearer),
    db: Session = Depends(get_db),
):
    if token:
        decodeJWT(token)
    return await UserController.register(request, authorization, db)


@routerUser.post("/login")
async def action(
    request: UserLogin,
    db: Session = Depends(get_db),
):
    return await UserController.login(request, db)

@routerUser.post("/verify_2fa")
async def action(
    request: Verify2FA,
    db: Session = Depends(get_db),
):
    return await UserController.verify_2fa(request, db)

@routerUser.post("/generate_otp/{token}")
async def action(
    token: str,
    db: Session = Depends(get_db),
):
    return await UserController.generate_otp(token, db)

@routerUser.get("", dependencies=[Depends(JWTBearer())])
async def action(
    authorization: str = Header(...),
    params: UserSearchParams = Depends(),
    page_params: PageParams = Depends(),
    db: Session = Depends(get_db),
):
    return await UserController.findAll(authorization, params, page_params, db)


# TODO: change method POST to GET
@routerUser.post("/profile", dependencies=[Depends(JWTBearer())])
async def action(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.profile(authorization, db)


@routerUser.put("/update-password", dependencies=[Depends(JWTBearer())])
async def action(
    request: PasswordUpdateByUsername,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.updatePasswordByUsername(request, authorization, db)


@routerUser.get("/{id}", dependencies=[Depends(JWTBearer())])
async def action(
    id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.find(id, authorization, db)


@routerUser.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def action(
    id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.delete(id, authorization, db)


@routerUser.put("/{id}", dependencies=[Depends(JWTBearer())])
async def action(
    request: UserUpdate,
    id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.update(id, request, authorization, db)


@routerUser.post("/update-password", dependencies=[Depends(JWTBearer())])
async def action(
    request: PasswordUpdate,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.updatePassword(request, authorization, db)


@routerUser.put("/update-password/{id}", dependencies=[Depends(JWTBearer())])
async def action(
    request: PasswordUpdate,
    id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    return await UserController.updatePasswordById(id, request, authorization, db)
