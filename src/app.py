import asyncio

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from .config import settings
from .events import on_shutdown, on_startup
from .logs import logs
from .oauth2 import endpoints as oauth2_endpoints
from .users import endpoints as users_endpoints
from .users.backends import TokenAuthenticationBackend


class Web:
    def __init__(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            docs_url="/api/openapi",
            openapi_url="/api/openapi.json",
            default_response_class=ORJSONResponse,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )
        self.web_server = None
        self.web_server_task = None
        self.bot_main_task = None

    def init_web(self):
        # Include API router
        self.app.include_router(users_endpoints.router, prefix="/api/users", tags=["users"])

        # Define aioauth-fastapi endpoints
        self.app.include_router(
            oauth2_endpoints.router,
            prefix="/oauth2",
            tags=["oauth2"],
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.add_middleware(AuthenticationMiddleware, backend=TokenAuthenticationBackend())

    async def start(self):
        import uvicorn

        self.init_web()
        self.web_server = uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                host=settings.PROJECT_HOST,
                port=settings.PROJECT_PORT,
                reload=settings.DEBUG,
            )
        )
        server_config = self.web_server.config
        server_config.setup_event_loop()
        if not server_config.loaded:
            server_config.load()
        self.web_server.lifespan = server_config.lifespan_class(server_config)
        try:
            await self.web_server.startup()
        except OSError as e:
            if e.errno == 10048:
                logs.error("Web Server 端口被占用：%s", e)
            logs.error("Web Server 启动失败，正在退出")
            raise SystemExit from None

        if self.web_server.should_exit:
            logs.error("Web Server 启动失败，正在退出")
            raise SystemExit from None
        logs.info("Web Server 启动成功")
        self.web_server_task = asyncio.create_task(self.web_server.main_loop())

    async def stop(self):
        if self.web_server_task:
            self.web_server_task.cancel()
        if self.bot_main_task:
            self.bot_main_task.cancel()


web = Web()
