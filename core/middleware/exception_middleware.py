import traceback

from starlette.requests import Request

from ..utils.http_error import InternalServerError


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
        traceback.print_exc()
        traceback.format_exc()
        # TODO: Add logging
        return InternalServerError().make_error_response()
