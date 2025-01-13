import re
import yaml


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