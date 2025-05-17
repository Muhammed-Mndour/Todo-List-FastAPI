from fastapi.requests import Request


async def before_request(request: Request, call_next):
    if request.url.path != '/hc':
        pass

    request.state.some_header = request.headers.get('some-header')

    res = await call_next(request)
    return res


def register_middleware(app):
    app.middleware('http')(before_request)
    return app
