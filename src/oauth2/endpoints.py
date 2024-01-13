from aioauth.config import Settings
from aioauth.oidc.core.grant_type import AuthorizationCodeGrantType
from aioauth.requests import Request as OAuth2Request
from aioauth.server import AuthorizationServer
from aioauth_fastapi.forms import TokenIntrospectForm
from aioauth_fastapi.utils import to_fastapi_response, to_oauth2_request, oidc_request_factory
from fastapi import APIRouter, Depends, Request

from .storage import Storage
from ..config import settings as local_settings
from ..storage.sqlalchemy import SQLAlchemyStorage, get_sqlalchemy_storage
from ..users.crypto import get_pub_key_resp
from ..utils.oauth import to_login_request

router = APIRouter()

settings = Settings(
    TOKEN_EXPIRES_IN=local_settings.ACCESS_TOKEN_EXP,
    REFRESH_TOKEN_EXPIRES_IN=local_settings.REFRESH_TOKEN_EXP,
    INSECURE_TRANSPORT=local_settings.DEBUG,
)
grant_types = {
    "authorization_code": AuthorizationCodeGrantType,
}


@router.post("/token")
async def token(
    request: Request,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage, grant_types=grant_types)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings, request_factory=oidc_request_factory)
    oauth2_response = await authorization_server.create_token_response(oauth2_request)
    return await to_fastapi_response(oauth2_response)


@router.post("/token/introspect")
async def token_introspect(
    request: Request,
    form: TokenIntrospectForm = Depends(),
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage, grant_types=grant_types)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_token_introspection_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)


@router.get("/authorize")
async def authorize(
    request: Request,
    storage: SQLAlchemyStorage = Depends(get_sqlalchemy_storage),
):
    if not request.user.is_authenticated:
        return await to_login_request(request)
    oauth2_storage = Storage(storage=storage)
    authorization_server = AuthorizationServer(storage=oauth2_storage, grant_types=grant_types)
    oauth2_request: OAuth2Request = await to_oauth2_request(request, settings)
    oauth2_response = await authorization_server.create_authorization_response(
        oauth2_request
    )
    return await to_fastapi_response(oauth2_response)


@router.get("/keys")
async def keys():
    return get_pub_key_resp()
