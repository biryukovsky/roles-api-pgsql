from aiohttp import web, hdrs


_TRUE = 'true'


def _parse_request_method(request: web.Request):
    """
    Parse Access-Control-Request-Method header of the preflight request
    """
    method = request.headers.get(hdrs.ACCESS_CONTROL_REQUEST_METHOD) or request.method.lower()
    return method


def _parse_request_headers(request: web.Request):
    """
    Parse Access-Control-Request-Headers header or the preflight request
    Returns set of headers in upper case.
    """
    headers = request.headers.get(hdrs.ACCESS_CONTROL_REQUEST_HEADERS)
    if headers is None:
        return frozenset()
    headers = (h.strip(" \t").upper() for h in headers.split(","))
    return frozenset(filter(None, headers))


async def _preflight_handler(request: web.Request, response: web.Response) -> web.Response:
    """CORS preflight response"""
    origin = request.headers.get(hdrs.ORIGIN) or request.headers.get(hdrs.HOST)

    request_method = _parse_request_method(request)
    request_headers = _parse_request_headers(request)

    response.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = origin
    response.headers[hdrs.ACCESS_CONTROL_ALLOW_CREDENTIALS] = _TRUE
    response.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = request_method

    if request_headers:
        response.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = ",".join(request_headers)
    return response


class CorsViewMixin:
    async def options(self):
        response = web.Response()
        response = await _preflight_handler(self.request, response)
        return response
