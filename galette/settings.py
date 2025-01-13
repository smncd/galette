from os import getenv
from pathlib import Path


DEBUG = getenv('DEBUG', False) in ('true', '1')

PAGES_DIR = Path(getenv('PAGES_DIR', '/pages'))
ASSETS_DIR = Path(getenv('ASSETS_DIR', '/assets'))
TEMPLATES_DIR = Path(getenv('TEMPLATES_DIR', '/templates'))
STATIC_DIR = Path(getenv('STATIC_DIR', '/static'))

for path in (PAGES_DIR, ASSETS_DIR, TEMPLATES_DIR, STATIC_DIR):
    if not path.exists() or not path.is_dir():
        raise ValueError(f"{path} is not a folder, exiting...")
