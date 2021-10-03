import traceback
import logging
from json import dumps, loads

from starlette.requests import Request

request_logger = logging.getLogger(__name__)


async def log_request(request: Request):
    """Function to log incoming request

    Args:
        request (Request): Request object.
    """

    if request.scope['method'] != 'GET':
        body = await request.json()
    else:
        body = None
    request_logger.info(
        "REQUEST",
        extra={
            'logType': 'REQUEST',
            "requestPath": request.scope['path'],
            "requestMethod": request.scope['method'],
            "requestBody": body if body else None,
            "requestQueryParams": str(request.scope['query_string']),
            "requestHost": request.headers.get('host'),
            "requestUserAgent": request.headers.get('user-agent'),
            "requestHeaders": dumps(dict(request.headers)),
        },
    )
