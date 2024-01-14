from typing import Optional

from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.config import settings
from src.users.crypto import encode_jwt, decode_jwt
from src.utils.redirect import RedirectResponseBuilder


async def to_login_request(request: Request) -> RedirectResponse:
    query_params = dict(request.query_params)
    params = ""
    for key, value in query_params.items():
        params += f"{key}={value}&"
    params = params[:-1]
    jwt = encode_jwt(settings.ACCESS_TOKEN_EXP, "", additional_claims={"params": params})
    resp = RedirectResponseBuilder()
    resp.set_cookie("SEND", jwt, max_age=settings.ACCESS_TOKEN_EXP)
    return resp.build("/api/users/login")


async def back_auth_request(
        request: Request,
        access_token: str = None,
        refresh_token: str = None,
) -> Optional[RedirectResponse]:
    cookie = request.cookies.get("SEND")
    if cookie is None:
        return None
    params = decode_jwt(cookie)["params"]
    resp = RedirectResponseBuilder()
    if access_token:
        resp.set_cookie("access_token", access_token, max_age=settings.ACCESS_TOKEN_EXP)
    if refresh_token:
        resp.set_cookie("refresh_token", refresh_token, max_age=settings.ACCESS_TOKEN_EXP)
    resp.delete_cookie("SEND")
    return resp.build(f"/oauth2/authorize?{params}", status_code=303)
