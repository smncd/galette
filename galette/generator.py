from os import getenv
from shutil import copytree
from jinja2 import Template
from starlette.requests import Request
from starlette.routing import Router
from galette.settings import ASSETS_DIR, STATIC_DIR, WEBP_DIR, PAGES_DIR
from galette.templates import templates
from galette.app import routes
from galette.files import get_all_page_files, get_file_content
from galette.pages import page_context
from galette.utils import set_path


def export():
    BUILD_DIR = set_path(
        path=getenv('GALETTE_BUILD_DIR'),
        fallback='.build',
        create_fallback=True
    )

    if not BUILD_DIR:
        raise Exception("Build dir does not exist, exiting...")

    router = Router(routes=routes)

    for page_path in get_all_page_files():
        request = Request(scope={
            'type': 'http',
            'router': router,
            'headers': {}
        })

        page_data = get_file_content(file=page_path)

        context = page_context(request, page_data)

        context['request'] = request

        template: Template = templates.get_template('page.jinja2')

        body = template.render(context)

        out_path = BUILD_DIR / page_path.relative_to(PAGES_DIR).with_suffix('' if page_path.name != 'index.md' else '.html') / ('index.html' if page_path.name != 'index.md' else '')

        out_path.parent.mkdir(exist_ok=True, parents=True)

        with (out_path).open('w') as file:
            file.write(body)
            file.close()
            print(file)
    
    for dir in (STATIC_DIR, ASSETS_DIR, WEBP_DIR):
        copytree(dir, BUILD_DIR / dir.name, dirs_exist_ok=True)
