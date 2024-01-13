from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response

from ..config import settings
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from .crud import SQLAlchemyCRUD
from .crypto import get_jwt
from .requests import UserLogin
from .responses import TokenResponse

router = APIRouter()
html = open("html/login.html", "r", encoding="utf-8").read()


@router.get("/login", name="users:login:get")
async def user_login_get():
    return Response(content=html, status_code=HTTPStatus.OK)


@router.post("/login", name="users:login")
async def user_login(
    response: Response,
    body: UserLogin,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    crud = SQLAlchemyCRUD(storage=storage)
    user = await crud.get(username=body.username)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    is_verified = user.verify_password(body.password)

    if is_verified:
        access_token, refresh_token = get_jwt(user)
        # NOTE: Setting expire causes an exception for requests library:
        # https://github.com/psf/requests/issues/6004
        response.set_cookie(
            key="access_token", value=access_token, max_age=settings.ACCESS_TOKEN_EXP
        )
        response.set_cookie(
            key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXP
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
