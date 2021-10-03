import traceback
import logging
from json import dumps, loads

from starlette.requests import Request
from ..utils import async_iterator_wrapper


response_logger = logging.getLogger(__name__)


async def log_response(request: Request, response, time_taken_milli):
    """Function to log response

    Args:
        request (Request): Request object
        response ([type]): Response object
        time_taken_milli ([type]): Time in millseconds
    """

    resp_body = {}
    if response.status_code / 100 != 2:
        resp_body = [section async for section in response.__dict__['body_iterator']]
        response.__setattr__('body_iterator', async_iterator_wrapper(resp_body))
        try:
            resp_body = loads(resp_body[0].decode())
        except:
            resp_body = str(resp_body)

    response_logger.info(
        "RESPONSE",
        extra={
            'logType': 'RESPONSE',
            "requestPath": request.scope['path'],
            "requestMethod": request.scope['method'],
            "requestQueryParams": str(request.scope['query_string']),
            "responseHeaders": dumps(dict(response.headers)),
            "responseStatusCode": response.status_code,
            "responseBody": resp_body,
            "responseTime": str(time_taken_milli),
        },
    )
