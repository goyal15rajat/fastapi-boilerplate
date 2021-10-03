import time
import traceback
from copy import deepcopy
from uuid import uuid4

import aiohttp
import requests
import ujson

from core.settings import app_configs

from .http_error import GatewayTimeout, InternalServerError
from .loggers.app_logger import app_logger


async def make_async_request(
    url,
    method,
    session=None,
    params=None,
    headers={},
    data=None,
    json=None,
    timeout=20,
    files=None,
    content_type=None,
    request_id=None,
    request_mask_map=None,
    connector=aiohttp.TCPConnector(limit=64, verify_ssl=False),
):
    '''Make async external request to a URL using python's request module.

    Args:
        url: URL of the request.
        method: method of the request.
        params: (optional) Dictionary or bytes to be sent in the query string.
        headers: (optional) Dictionary of HTTP Headers to send.
        data: (optional) Dictionary or list of tuples, bytes, or file-like object to send in the body.
        json: (optional) A JSON serializable Python object to send in the body.
        timeout: (optional) How many seconds to wait for the server to send data.
        files: (optional) File object.
        content_type: (optional) request content type.
        request_id: (optional) Id of the request.
        request_mask_map: Dictionary of request objects which needs to be hidden. (Level 1 hiding only)
        eg - {
            'params' : ['key1', 'key2']
        }

    Returns:
        A tuple containing response of the request in JSON format, binary format and HTTP code of the response and
        message of the error in making request (if any).
    '''

    request_id = str(uuid4())
    response_json = {}
    response_content = None
    response_code = None
    error = None

    req = {}

    if headers:
        req.update({'headers': headers})

    if params:
        req.update({'params': params})

    if data:
        req.update({'data': data})

    if json:
        req.update({'json': json})

    if timeout:
        req.update({'timeout': timeout})

    request_dict = deepcopy(req)

    if files:
        req.update({'files': files})

        files_req = {key: value.name for (key, value) in files.items()}

        request_dict.update({'files': files_req})

    try:
        if request_mask_map:
            for request_attr, hidden_key_list in request_mask_map.items():
                for hidden_key in hidden_key_list:
                    if request_dict.get(request_attr, {}).get(hidden_key, None):
                        request_dict[request_attr][hidden_key] = '## HIDDEN ##'
    except Exception:
        app_logger.exception('API_ERROR_WHILE_MASKING')

    app_logger.info(
        'API_REQUEST',
        extra={
            'meta': {
                'logType': 'APP',
                'requestPath': url,
                'requestMethod': method,
                'requestDict': ujson.dumps(request_dict),
                'requestId': request_id,
            }
        },
    )

    if not session:
        session = aiohttp.ClientSession(connector=connector)

    try:
        request_epoch = time.time() * 1000
        async with session:
            response = await session.request(method, url, **req)

            response_code = response.status

            response_content = await response.text()
            if response_content:
                if content_type:
                    response_json = await response.json(content_type=content_type)
                else:
                    response_json = await response.json()
            else:
                response_json = {}

        response_epoch = time.time() * 1000

        app_logger.info(
            'API_RESPONSE',
            extra={
                'meta': {
                    'logType': 'APP',
                    'responseCode': response_code,
                    'responseTime': str(response_epoch - request_epoch),
                    'responseContent': (
                        response_content if (int(response_code / 100) != 2 or app_configs.DEBUG) else "{}"
                    ),
                    'requestId': request_id,
                }
            },
        )

    except ValueError:
        app_logger.exception('API_ERROR')
        raise InternalServerError()

    except requests.exceptions.ReadTimeout:
        app_logger.exception('API_TIMEOUT_ERROR')
        raise GatewayTimeout()

    except Exception:
        app_logger.exception('API_ERROR')
        raise InternalServerError()

    return (response_json, response_content, response_code, error)
