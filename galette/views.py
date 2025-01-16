from uuid import uuid5, NAMESPACE_URL
from img2webp import convert_image
from pathlib import Path
from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from markdown import markdown
from bs4 import BeautifulSoup
from markupsafe import Markup

from galette.cache import PageCache
from galette.files import get_file_content
from galette.settings import PAGES_DIR, ASSETS_DIR, WEBP_DIR, DEBUG
from galette.templates import render, html_ext_list
from galette.pages import page_context


cache = PageCache(maxsize=512)


def not_found(request: Request, exc: HTTPException) -> HTMLResponse:
    response, _ = render(
        request=request,
        name=html_ext_list('404'),
        status_code=404,
    )

    return response


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
        
        headers = {}
        body: str
        
        page_id = page_path.as_uri()
        page_file_mtime = page_path.stat().st_mtime
        
        page_cache = cache.get(id=page_id)

        if not DEBUG and page_cache and page_cache['timestamp'] >= page_file_mtime and page_file_mtime - page_cache['timestamp'] < page_cache['ttl']:
            body = page_cache['body']
            headers['Is-Cached'] = 'true'
        else:
            context = {}
        
            page_data = get_file_content(file=page_path)

            context = page_context(request, page_data)

            _, body = render(
                request=request, 
                name=html_ext_list('page'),
                context=context,
            )

            if not DEBUG:
                cache.set(id=page_id, ttl=300, timestamp=page_file_mtime, body=body)

        return HTMLResponse(
            content=body,
            headers=headers
        )
    