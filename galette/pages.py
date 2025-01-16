from uuid import uuid5, NAMESPACE_URL
from img2webp import convert_image
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
from markupsafe import Markup
from starlette.requests import Request
from galette.settings import ASSETS_DIR, WEBP_DIR


def page_context(request: Request|dict, page_data: dict[str, dict|str]) -> dict:
    context = {}

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

    frontmatter = page_data['frontmatter']

    if frontmatter:
        for key, value in frontmatter.items():
            context[key] = value

    return context