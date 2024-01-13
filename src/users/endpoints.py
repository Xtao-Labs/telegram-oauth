from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.requests import Request

from .crud import SQLAlchemyCRUD
from .crypto import get_jwt
from .responses import TokenResponse
from ..config import settings
from ..html import templates
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from ..utils.oauth import back_auth_request
from ..utils.telegram import verify_telegram_auth_data

router = APIRouter()


@router.get("/login", name="users:login:get")
async def user_login_get(request: Request):
    url = request.url
    callback_url = str(url).replace("/login", "/callback")
    return templates.TemplateResponse("login.jinja", {"request": request, "callback_url": callback_url})


@router.get("/callback", name="users:login")
async def user_login(
        request: Request,
        response: Response,
        storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    tg_id = await verify_telegram_auth_data(request.query_params)
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
    response.set_cookie(
        key="access_token", value=access_token, max_age=settings.ACCESS_TOKEN_EXP
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, max_age=settings.REFRESH_TOKEN_EXP
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
