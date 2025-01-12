import re
import yaml
from typing import Any, TypedDict
from time import time
from os import getenv
from pathlib import Path
from starlette.templating import Jinja2Templates
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from markdown import markdown
from bs4 import BeautifulSoup
from markupsafe import Markup


DEBUG = getenv('DEBUG', False) in ('true', '1')

PAGES_DIR = Path(getenv('PAGES_DIR', '/pages'))
ASSETS_DIR = Path(getenv('ASSETS_DIR', '/assets'))
TEMPLATES_DIR = Path(getenv('TEMPLATES_DIR', '/templates'))
STATIC_DIR = Path(getenv('STATIC_DIR', '/static'))

for path in (PAGES_DIR, ASSETS_DIR, TEMPLATES_DIR, STATIC_DIR):
    if not path.exists() or not path.is_dir():
        raise ValueError(f"{path} is not a folder, exiting...")


class PageCacheItem(TypedDict):
    ttl: int
    timestamp: float
    body: str

class PageCache:
    _store: dict[str, PageCacheItem] = {}

    def set(self, id: str, **item: PageCacheItem):
        self._store[id] = item
        
    def get(self, id: str) -> PageCacheItem|None:
        return self._store[id] if id in self._store else None


def get_file_content(file: str) -> dict[str, dict|str|None]:
    frontmatter_regex = re.compile(r'^\A(?:---|\+\+\+)(.*?)(?:---|\+\+\+)\n', re.S | re.M)

    frontmatter_result = frontmatter_regex.search(file)

    frontmatter = []
    content = re.sub(r'^\A---\n([\s\S]*?)\n---\n', '', file)

    if frontmatter_result:
        try:
            frontmatter = yaml.load(
                stream=frontmatter_result.group(1),
                Loader=yaml.FullLoader
            )
        except:
            pass
    
    return {
        'frontmatter': frontmatter,
        'content': content
    }


templates = Jinja2Templates(directory=TEMPLATES_DIR)

cache = PageCache()


def not_found(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request=request,
        name='404.jinja2',
        status_code=404,
    )

class Page(HTTPEndpoint):
    async def get(self, request: Request) -> HTMLResponse:       
        page = request.path_params['page']

        if page == "":
            page = 'index'

        if page.endswith(('/index.html', '.html', '.md')):
            return RedirectResponse(
                url=f"/{page.removesuffix('/index.html').removesuffix('.html').removesuffix('.md')}",
                status_code=308,
            )

        page = page.strip('/') + '.md'

        page_path = PAGES_DIR / page

        if not page_path.is_file():
            raise HTTPException(
                status_code=404
            ) 
        
        body: str
        
        page_id = page_path.as_uri()
        page_file_mtime = page_path.stat().st_mtime
        
        page_cache = cache.get(id=page_id)

        if page_cache and page_cache['timestamp'] >= page_file_mtime and page_cache['timestamp'] < page_cache['ttl']:
            body = page_cache['body']
        else:
            context = {}
        
            page_file = open(page_path, 'r').read()

            page_data = get_file_content(file=page_file)

            html = markdown(
                text=page_data['content'],
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

            context['html'] = Markup(soup.prettify())
            context['page_path'] = page_path

            frontmatter = page_data['frontmatter']

            if frontmatter:
                for key, value in frontmatter.items():
                    context[key] = value

            body = templates.TemplateResponse(
                request=request, 
                name='page.jinja2',
                context=context
            ).body

            cache.set(id=page_id, ttl=300, timestamp=page_file_mtime, body=body)

        return HTMLResponse(
            content=body
        )
    

routes = [
    Mount('/static', StaticFiles(directory=STATIC_DIR), name='static'),
    Mount('/assets', StaticFiles(directory=ASSETS_DIR), name='assets'),
    Route('/{page:path}', Page, name='page'),
]

exception_handlers = {
    404: not_found
}

app = Starlette(routes=routes, exception_handlers=exception_handlers, debug=DEBUG)
