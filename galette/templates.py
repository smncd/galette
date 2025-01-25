from typing import Any, Tuple
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.requests import Request
from jinja2.exceptions import TemplateNotFound

from galette.settings import TEMPLATES_DIR


templates = Jinja2Templates(directory=TEMPLATES_DIR)


def html_ext_list(id: str) -> list[str]:
    extensions = [
        'html.jinja2',
        'html.jinja',
        'jinja2',
        'jinja',
        'html',
    ]

    return [f"{id}.{extension}" for extension in extensions]


def render(request: Request, name: str | list[str], **kwargs: Any) -> Tuple[_TemplateResponse, bytes | memoryview]:
    template_res = lambda tname: templates.TemplateResponse(
        request=request, name=tname, **kwargs
    )

    if isinstance(name, str):
        try:
            res = template_res(name)
            return res, res.body
        except TemplateNotFound:
            raise TemplateNotFound(f"Template '{name}' was not found.")
    else:
        for template_name in name:
            try:
                res = template_res(template_name)
                return res, res.body
            except TemplateNotFound:
                continue

    raise TemplateNotFound("None of the provided templates were found.")