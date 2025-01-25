from starlette.applications import Starlette
from galette.settings import DEBUG
from galette.routes import routes, exception_handlers

app = Starlette(routes=routes, exception_handlers=exception_handlers, debug=DEBUG)
