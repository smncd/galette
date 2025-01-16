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

            for img in soup.find_all('img', src=True):
                if img['src'].startswith('/assets'):
                    path = Path(img['src'].removeprefix('/assets/'))
                    
                    asset_path: Path = ASSETS_DIR / path

                    if not asset_path.is_file():
                        continue

                    asset_name = asset_path.name
                    asset_timestamp = asset_path.stat().st_mtime

                    asset_name_hash = asset_name
                    asset_time_hash = str(uuid5(namespace=NAMESPACE_URL, name=str(asset_timestamp)))

                    webp_name = f'{asset_time_hash}.webp'
                    
                    webp_path = WEBP_DIR / path.with_name(asset_name_hash) / webp_name
                    webp_path.parent.mkdir(parents=True, exist_ok=True)

                    webp_src = request.url_for('webp_assets', path=str(path.with_name(asset_name_hash) / webp_name))

                    if not webp_path.is_file():
                        for path in webp_path.parent.rglob('**/*'):
                            if path.is_file():
                                path.unlink()
            
                        convert_image(asset_path, webp_path, quality=80)

                    picture_tag = soup.new_tag('picture')

                    source_tag = soup.new_tag('source')
                    source_tag.attrs['srcset'] = webp_src
                    source_tag.attrs['type'] = 'image/webp'
                    picture_tag.append(source_tag)

                    img_tag = soup.new_tag('img')
                    img_tag.attrs = img.attrs
                    img_tag.attrs['src'] = request.url_for('assets', path=img.attrs['src'])
                    picture_tag.append(img_tag)

                    img.replace_with(picture_tag)


            context['html'] = Markup(soup.prettify())
            context['page_path'] = page_path

            frontmatter = page_data['frontmatter']

            if frontmatter:
                for key, value in frontmatter.items():
                    context[key] = value

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
    