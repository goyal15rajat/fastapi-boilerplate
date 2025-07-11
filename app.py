import os
from contextlib import asynccontextmanager
from logging.config import dictConfig

import socketio
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from core.connections.mongo import MongoConnectionSingleton
from core.connections.redis_manager import redis_cache
from core.middleware.exception_middleware import catch_exceptions_middleware
from core.middleware.logger_middleware import api_req_res_logger
from core.routes import api_router as core_router
from core.settings import app_configs
from core.utils.dependencies import log_request_json
from core.utils.http_error import (
    BadRequest,
    Forbidden,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    ServiceUnavailable,
    Unauthorized,
    Unprocessable,
    http_error_handler,
)
from webapp.routes import ui_router as webapp_router
from ws_app.app_event import AppEventNamespace

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dictConfig(app_configs.LOGGING_CONFIG)


# To start redis and mongo on service bootup
@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = MongoConnectionSingleton()
    await connection.connect()
    redis_cache.init_redis()
    yield
    await connection.close()


app = FastAPI(
    title="FastApi bolierplate",
    description="FastApi bolierplate",
    debug=app_configs.DEBUG,
    lifespan=lifespan,
    contact={
        "name": "",
        "url": "http://host.example.com/api/",
    },
    docs_url=f"/{app_configs.APP_NAME}/api{app_configs.DOCS_URL}" if app_configs.DOCS_URL else None,
    redoc_url=f"/{app_configs.APP_NAME}/api{app_configs.REDOC_URL}" if app_configs.REDOC_URL else None,
)

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    async_handlers=True,
    engineio_logger=app_configs.DEBUG,
    ping_interval=app_configs.PING_INTERVAL,
    ping_timeout=app_configs.PING_TIMEOUT,
)
sio.register_namespace(AppEventNamespace('/event'))
socket_app = socketio.ASGIApp(sio, socketio_path=f'/{app_configs.APP_NAME}/ws/socket.io')

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount(f"/{app_configs.APP_NAME}/ws/socket.io", socket_app)  # Mounting Socket.IO app at /boilerplate/ws

# Registering error handlers
app.add_exception_handler(BadRequest, http_error_handler)
app.add_exception_handler(Unauthorized, http_error_handler)
app.add_exception_handler(Forbidden, http_error_handler)
app.add_exception_handler(NotFound, http_error_handler)
app.add_exception_handler(MethodNotAllowed, http_error_handler)
app.add_exception_handler(Unprocessable, http_error_handler)
app.add_exception_handler(InternalServerError, http_error_handler)
app.add_exception_handler(ServiceUnavailable, http_error_handler)

app.include_router(webapp_router, prefix=f"/{app_configs.APP_NAME}/app")  # UI routes without prefix for direct access
app.include_router(core_router, prefix=f"/{app_configs.APP_NAME}", dependencies=[Depends(log_request_json)])

app.middleware('http')(catch_exceptions_middleware)
app.middleware('http')(api_req_res_logger)
