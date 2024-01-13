from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response, Form
from starlette.requests import Request

from .crud import SQLAlchemyCRUD
from .crypto import get_jwt
from .responses import TokenResponse
from ..config import settings
from ..html import templates
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from ..utils.oauth import back_auth_request

router = APIRouter()


@router.get("/login", name="users:login:get")
async def user_login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", name="users:login")
async def user_login(
    request: Request,
    response: Response,
    username: str = Form(),
    password: str = Form(),
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    crud = SQLAlchemyCRUD(storage=storage)
    user = await crud.get(username=username)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    is_verified = user.verify_password(password)

    if is_verified:
        access_token, refresh_token = get_jwt(user)
        # NOTE: Setting expire causes an exception for requests library:
        # https://github.com/psf/requests/issues/6004
        if resp := await back_auth_request(request, access_token, refresh_token):
            return resp
        response.set_cookie(
            key="access_token", value=access_token, max_age=settings.ACCESS_TOKEN_EXP
        )
        response.set_cookie(
            key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXP
        )
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
