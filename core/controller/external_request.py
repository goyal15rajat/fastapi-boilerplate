from fastapi import APIRouter

from core.utils.http_response import OK
from core.utils.request_client import make_async_request

router = APIRouter()


@router.get("/")
async def make_external_request():
    """Api to manage version

    Response -
    {
        "data": {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg"
        },
        "support": {
            "url": "https://reqres.in/#support-heading",
            "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
        },
        "metadata": {}
    }
    """
    response_json, response_content, response_code, error = await make_async_request(
        url='https://reqres.in/api/users/2', method='GET', timeout=4
    )

    return OK(response_json)
