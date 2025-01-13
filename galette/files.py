import re
import yaml
from pathlib import PosixPath

from galette.settings import PAGES_DIR

def get_all_page_files() -> list[PosixPath]:
    return list(PAGES_DIR.rglob('*.md'))


def get_file_content(file: str) -> dict[str, dict|str|None]:
    frontmatter_regex = re.compile(r'^\A(?:---|\+\+\+)(.*?)(?:---|\+\+\+)', re.S | re.M)

    frontmatter_result = frontmatter_regex.search(file)

    frontmatter = []
    content = re.sub(r'^\A---\n([\s\S]*?)\n---', '', file)

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