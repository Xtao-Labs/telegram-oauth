from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError
from starlette.requests import Request

from .crud import SQLAlchemyCRUD
from .crypto import get_jwt
from ..config import settings
from ..html import templates
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from ..utils.oauth import back_auth_request
from ..utils.redirect import RedirectResponseBuilder
from ..utils.telegram import decode_telegram_auth_data, verify_telegram_auth_data

router = APIRouter()


@router.get("/login", name="users:login:get")
async def user_login_get(request: Request):
    if request.user.is_authenticated:
        if resp := await back_auth_request(request):
            return resp
        return RedirectResponseBuilder().build(settings.PROJECT_LOGIN_SUCCESS_URL)
    url = request.url
    callback_url = str(url).replace("/login", "/callback")
    return templates.TemplateResponse(
        "login.jinja",
        {"request": request, "callback_url": callback_url, "username": settings.BOT_USERNAME}
    )


async def auth(
        tg_id: int,
        request: Request,
        storage: SQLAlchemyStorage,
):
    if tg_id is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    crud = SQLAlchemyCRUD(storage=storage)
    user = await crud.get_by_tg_id(tg_id=tg_id)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    access_token, refresh_token = get_jwt(user)
    # NOTE: Setting expire causes an exception for requests library:
    # https://github.com/psf/requests/issues/6004
    if resp := await back_auth_request(request, access_token, refresh_token):
        return resp
    resp = RedirectResponseBuilder()
    resp.set_cookie(
        key="access_token", value=access_token, max_age=settings.ACCESS_TOKEN_EXP
    )
    resp.set_cookie(
        key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXP
    )
    return resp.build(settings.PROJECT_LOGIN_SUCCESS_URL)


@router.get("/callback", name="users:login")
async def user_login(
        request: Request,
        storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    tg_id = await verify_telegram_auth_data(request.query_params)
    return await auth(tg_id, request, storage)


@router.get("/auth", name="users:auth")
async def user_auth(
        request: Request,
        storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    try:
        tg_id = await decode_telegram_auth_data(request.query_params)
    except JWTError:
        tg_id = None
    return await auth(tg_id, request, storage)
