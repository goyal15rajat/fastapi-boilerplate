import traceback
import logging
from json import dumps, loads

from starlette.requests import Request

from fastapi.params import Header

request_logger = logging.getLogger(__name__)


async def log_request(request: Request):
    """Function to log incoming request

    Args:
        request (Request): Request object.
    """

    request_logger.info(
        "REQUEST",
        extra={
            "logType": "REQUEST",
            "requestPath": request.scope["path"],
            "requestMethod": request.scope["method"],
            "requestBody": "check REQUEST_PAYLOAD log",
            "requestQueryParams": str(request.scope["query_string"]),
            "requestHost": request.headers.get("host"),
            "requestUserAgent": request.headers.get("user-agent"),
            "requestHeaders": dumps(dict(request.headers)),
        },
    )
