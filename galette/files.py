import re
import yaml
from pathlib import Path

from galette.settings import PAGES_DIR

def get_all_page_files() -> list[Path]:
    return list(PAGES_DIR.rglob('*.md'))


def get_file_content(file: Path) -> dict[str, dict|str|None]:
    data = open(file, 'r').read()

    frontmatter_regex = re.compile(r'^\A(?:---|\+\+\+)(.*?)(?:---|\+\+\+)', re.S | re.M)

    frontmatter_result = frontmatter_regex.search(data)

    frontmatter = []
    content = re.sub(r'^\A---\n([\s\S]*?)\n---', '', data)

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