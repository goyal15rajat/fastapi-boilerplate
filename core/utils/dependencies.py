from fastapi import Request
from .loggers.app_logger import app_logger


async def log_request_json(request: Request):
    """Dependecy function to log request json

    Args:
        request (Request): Request Object
    """

    try:
        if getattr(request, '_json', None):
            app_logger.info(
                "REQUEST_PAYLOAD",
                extra={
                    "meta": {
                        "requestBody": request._json,
                        "requestPath": request.scope["path"],
                        "requestMethod": request.scope["method"],
                        "requestQueryParams": str(request.scope["query_string"]),
                    }
                },
            )
    except Exception:
        app_logger.exception('JSON_BODY_LOGGER')
