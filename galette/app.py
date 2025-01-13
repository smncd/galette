from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from galette.settings import STATIC_DIR, ASSETS_DIR, DEBUG
from galette.views import Page, not_found


routes = [
    Mount('/static', StaticFiles(directory=STATIC_DIR), name='static'),
    Mount('/assets', StaticFiles(directory=ASSETS_DIR), name='assets'),
    Route('/{page:path}', Page, name='page'),
]

exception_handlers = {
    404: not_found
}

app = Starlette(routes=routes, exception_handlers=exception_handlers, debug=DEBUG)
