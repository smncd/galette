from os import getenv
from pathlib import Path
from starlette.templating import Jinja2Templates
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from markdown import markdown
from bs4 import BeautifulSoup
from markupsafe import Markup



DEBUG = getenv('DEBUG', False) in ('true', '1')

PAGES_DIR = Path('/pages')


templates = Jinja2Templates(directory='templates')


def not_found(request, exc: HTTPException):
    return templates.TemplateResponse(
        request=request,
        name='404.jinja2',
        status_code=404,
    )

class Page(HTTPEndpoint):
    async def get(self, request):
        page = request.path_params['page']

        if page == "":
            page = 'index'

        page = page.replace('/index.html', '').removesuffix('.html').removesuffix('.md').strip('/') + '.md'

        page_path = PAGES_DIR / page

        if not page_path.is_file():
            raise HTTPException(
                status_code=404
            ) 

        page_file = open(page_path, 'r')

        html = markdown(
            text=page_file.read(), 
            extensions=[
                'attr_list',
                'def_list',
                'fenced_code',
                'footnotes',
                'tables',
                'toc',
            ],
        )

        soup = BeautifulSoup(html, "html.parser")

        for anchor in soup.find_all('a', href=True):
            if anchor['href'].endswith('.md'):
                anchor['href'] = anchor['href'][:-3]

        html = Markup(soup.prettify())

        return templates.TemplateResponse(
            request=request, 
            name='page.jinja2',
            context={
                'html': html,
                'page_path': page_path
            }
        )
    

routes = [
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Mount('/assets', StaticFiles(directory='/assets'), name='assets'),
    Route('/{page:path}', Page, name='page'),
]

exception_handlers = {
    404: not_found
}

app = Starlette(routes=routes, exception_handlers=exception_handlers, debug=DEBUG)
