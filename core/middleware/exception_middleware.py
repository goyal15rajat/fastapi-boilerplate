from starlette.requests import Request
from starlette.responses import JSONResponse
from ..utils.http_error import InternalServerError
import traceback


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
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "error": {
                    "message": "Looks like something went wrong! Please try again.\nIf the issue persists please contact support.",
                    "errors": {},
                    "title": "",
                    "error_subcode": 0,
                },
                "metadata": {},
            },
        )
