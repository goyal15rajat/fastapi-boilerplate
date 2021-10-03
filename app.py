import os
from logging.config import dictConfig

from fastapi import FastAPI

from core.middleware.exception_middleware import catch_exceptions_middleware
from core.middleware.logger_middleware import api_req_res_logger
from core.routes import api_router as core_router
from core.settings import app_configs
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dictConfig(app_configs.LOGGING_CONFIG)

app = FastAPI(
    title="FastApi bolierplate",
    description="FastApi bolierplate",
    debug=app_configs.DEBUG,
    contact={
        "name": "",
        "url": "http://host.example.com/api/",
    },
    docs_url=f"/api/{app_configs.APP_NAME}{app_configs.DOCS_URL}" if app_configs.DOCS_URL else None,
    redoc_url=f"/api/{app_configs.APP_NAME}{app_configs.REDOC_URL}" if app_configs.REDOC_URL else None,
)


# Registering error handlers
app.add_exception_handler(BadRequest, http_error_handler)
app.add_exception_handler(Unauthorized, http_error_handler)
app.add_exception_handler(Forbidden, http_error_handler)
app.add_exception_handler(NotFound, http_error_handler)
app.add_exception_handler(MethodNotAllowed, http_error_handler)
app.add_exception_handler(Unprocessable, http_error_handler)
app.add_exception_handler(InternalServerError, http_error_handler)
app.add_exception_handler(ServiceUnavailable, http_error_handler)

app.include_router(core_router, prefix=f"/api/{app_configs.APP_NAME}")

app.middleware('http')(catch_exceptions_middleware)
app.middleware('http')(api_req_res_logger)
