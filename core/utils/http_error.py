from starlette.requests import Request
from starlette.responses import JSONResponse

"""
USE: from core.utils.http_error import InternalServerError

...
raise InternalServerError(message: "example message", "error_subcode": -1, errors={}, title="Example title")
...

"""


class HTTPError(Exception):
    """Http Error Exception to be extended for various Http error status codes"""

    def __init__(self, message: str, status_code: int, error_subcode: int = 0, errors={}, title: str = ''):
        self.status_code = status_code
        self.error_subcode = error_subcode
        self.message = message
        self.errors = errors
        self.title = title
        self.response_json = {
            'statusCode': self.status_code,
            'error': {
                'message': self.message,
                'errors': self.errors,
                'title': self.title,
                'error_subcode': self.error_subcode,
            },
            'metadata': {},
        }

    def make_error_response(self):
        """Method to return response json

        Returns:
            [JSONResponse]: Error response
        """
        return JSONResponse(self.response_json, status_code=self.status_code)


async def http_error_handler(request: Request, exc: HTTPError) -> JSONResponse:
    """Function to return response for http error"""
    return JSONResponse(
        content=exc.response_json,
        status_code=exc.status_code,
    )


class BadRequest(HTTPError):
    """Exception for HTTP 400 extended from HttpError

    The server cannot or will not process the request due to an apparent client error.
    """

    def __init__(
        self,
        message: str = 'The request is invalid. Please try again.',
        status_code: int = 400,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class Unauthorized(HTTPError):
    """Exception for HTTP 401 extended from HttpError

    Use when authentication is required and has failed or has not yet been provided.
    Basically when access to resource needs login
    """

    def __init__(
        self,
        message='Sent request is unauthorized. Please log in first.',
        status_code: int = 401,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class Forbidden(HTTPError):
    """Exception for HTTP 403 extended from HttpError

    The user might be logged in but does not have the necessary permissions for the resource.
    """

    def __init__(
        self,
        message: str = 'You don\'t have necessary permissions to access this resource.',
        status_code: int = 403,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class NotFound(HTTPError):
    """Exception for HTTP 404 extended from HttpError

    The requested resource could not be found but may be available in future.
    """

    def __init__(
        self,
        message='The resource you are looking for does not exist.',
        status_code: int = 404,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class MethodNotAllowed(HTTPError):
    """Exception for HTTP 405 extended from HttpError

    A request method is not supported for the requested resource.
    """

    def __init__(
        self,
        message: str = 'This method is not allowed for the sent request.',
        status_code: int = 405,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class Unprocessable(HTTPError):
    """Exception for HTTP 422 extended from HttpError

    Unprocessable Entity.
    """

    def __init__(
        self,
        message='Unprocessable Entity! Please try again later.',
        status_code: int = 422,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class InternalServerError(HTTPError):
    """Exception for HTTP 500 extended from HttpError

    A generic error message, error_code=None, given when an unexpected condition was encountered and no more specific
    message is suitable.
    """

    def __init__(
        self,
        message: str = 'Looks like something went wrong! Please try again.\nIf the issue persists please contact support.',
        status_code: int = 500,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class GatewayTimeout(HTTPError):
    """Exception for HTTP 504 extended from HttpError

    A generic error message, given when web server didn’t receive a timely response from another server upstream when it attempted to load one of your web resource.
    """

    def __init__(
        self,
        message: str = 'Cant connect to server at this moment.\nIf the issue persists please contact support.',
        status_code: int = 504,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)


class ServiceUnavailable(HTTPError):
    """Exception for HTTP 503 extended from HttpError

    The service being requested is not available .
    """

    def __init__(
        self,
        message='Service is currently unavailable. Please contact support if issue persists.',
        status_code: int = 503,
        error_subcode: int = 0,
        errors={},
        title: str = '',
    ):
        super().__init__(message, status_code, error_subcode, errors, title)
