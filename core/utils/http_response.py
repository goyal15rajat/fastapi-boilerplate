from fastapi.responses import JSONResponse, Response


class OK(JSONResponse):
    """A Custom JSONResponse class that append response with 200 http status_code code."""

    def __init__(self, data: dict = {}, **kwargs):
        """
        Args:
            data: Data to be dumped into JSON. By default only dict objects
                  are allowed to be passed due to a security flaw.
            encoder: A JSON encoder class.
            safe: Controls if only dict objects may be serialized. Defaults to True.
            json_dumps_params: A dictionary of kwargs passed to json.dumps().
            kwargs: key word args for Django's JsonResponse class (params of HttpResponseBase class)
        """

        kwargs['status_code'] = 200
        data['metadata'] = {**data.get('metadata', {})}

        super().__init__(data, **kwargs)


class Created(JSONResponse):
    """A Custom JSONResponse class that append response with 201 http status_code code."""

    def __init__(self, data: dict = {}, **kwargs):
        """
        Args:
            data: Data to be dumped into JSON. By default only dict objects
                  are allowed to be passed due to a security flaw.
            encoder: A JSON encoder class.
            safe: Controls if only dict objects may be serialized. Defaults to True.
            json_dumps_params: A dictionary of kwargs passed to json.dumps().
            kwargs: key word args for Django's JsonResponse class (params of HttpResponseBase class)
        """

        kwargs['status_code'] = 201
        data['metadata'] = {**data.get('metadata', {})}

        super().__init__(data, **kwargs)


class Accepted(JSONResponse):
    """A Custom JSONResponse class that append response with 202 http status_code code."""

    def __init__(self, data: dict = {}, **kwargs):
        """
        Args:
            data: Data to be dumped into JSON. By default only dict objects
                  are allowed to be passed due to a security flaw.
            encoder: A JSON encoder class.
            safe: Controls if only dict objects may be serialized. Defaults to True.
            json_dumps_params: A dictionary of kwargs passed to json.dumps().
            kwargs: key word args for Django's JsonResponse class (params of HttpResponseBase class)
        """

        kwargs['status_code'] = 202
        data['metadata'] = {**data.get('metadata', {})}

        super().__init__(data, **kwargs)


class NoContent(Response):
    """A Custom JSONResponse class that append response with 204 http status_code code."""

    def __init__(self, **kwargs):
        kwargs['status_code'] = 204
        data['metadata'] = {**data.get('metadata', {})}

        super().__init__(headers={}, **kwargs)
