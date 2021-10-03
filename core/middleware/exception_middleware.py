import traceback

from starlette.requests import Request

from ..utils.http_error import InternalServerError
from ..utils.loggers.app_logger import app_logger


async def catch_exceptions_middleware(request: Request, call_next):
    """Middleware to handle global exception

    Args:
        request (Request): [description]
        call_next ([type]): [description]

    Returns:
        [Response]: [InternalServerError]
    """

    try:
        return await call_next(request)
    except Exception:
        app_logger.exception('ERROR')
        return InternalServerError().make_error_response()
