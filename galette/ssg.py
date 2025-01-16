from shutil import copytree
from jinja2 import Template
from starlette.requests import Request
from starlette.routing import Router
from galette.settings import BUILD_DIR, ASSETS_DIR, STATIC_DIR, WEBP_DIR
from galette.templates import templates
from galette.app import routes
from galette.files import get_all_page_files, get_file_content
from galette.pages import page_context


if __name__ == '__main__':
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

        page_path_name = page_path.with_suffix('').name

        out_path = BUILD_DIR / (page_path_name if page_path_name != 'index' else '') / 'index.html' 

        out_path.parent.mkdir(exist_ok=True, parents=True)

        with (out_path).open('w') as file:
            file.write(body)
            file.close()
            print(file)

    copytree(STATIC_DIR, BUILD_DIR / STATIC_DIR.name, dirs_exist_ok=True)
    copytree(ASSETS_DIR, BUILD_DIR / ASSETS_DIR.name, dirs_exist_ok=True)
    copytree(WEBP_DIR, BUILD_DIR / WEBP_DIR.name, dirs_exist_ok=True)
