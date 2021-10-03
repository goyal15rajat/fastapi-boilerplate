import logging
import time
import traceback
from json import dumps, loads

from starlette.requests import Request

from ..utils.http_error import InternalServerError
from ..utils.loggers.request_logger import log_request
from ..utils.loggers.response_logger import log_response


async def api_req_res_logger(request: Request, call_next):
    """Middleware to handle global exception

    Args:
        request (Request): [description]
        call_next ([type]): [description]

    Returns:
        [Response]: [InternalServerError]
    """

    try:
        request_epoch_milli = time.time() * 1000
        await log_request(request)
        response = await call_next(request)
        time_taken_milli = time.time() * 1000 - request_epoch_milli
        await log_response(request, response, time_taken_milli)
        return response
    except Exception:
        traceback.print_exc()
        traceback.format_exc()
        # TODO: Add logging
        return InternalServerError().make_error_response()
