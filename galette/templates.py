from starlette.templating import Jinja2Templates
from galette.settings import TEMPLATES_DIR


templates = Jinja2Templates(directory=TEMPLATES_DIR)
