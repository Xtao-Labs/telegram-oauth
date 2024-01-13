import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .events import on_shutdown, on_startup
from .oauth2 import endpoints as oauth2_endpoints
from .users import endpoints as users_endpoints
from .users.backends import TokenAuthenticationBackend

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
)

# Include API router
app.include_router(users_endpoints.router, prefix="/api/users", tags=["users"])

# Define aioauth-fastapi endpoints
app.include_router(
    oauth2_endpoints.router,
    prefix="/oauth2",
    tags=["oauth2"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())
