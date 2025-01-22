from os import getenv
from galette.utils import set_path

DEBUG = getenv('DEBUG', False) in ('true', '1')

PAGES_DIR = set_path(
    path=getenv('GALETTE_PAGES_DIR'),
    fallback='pages'
)

ASSETS_DIR = set_path(
    path=getenv('GALETTE_ASSETS_DIR'),
    fallback='assets'
)

WEBP_DIR = set_path(
    path=getenv('GALETTE_WEBP_DIR'),
    fallback='.webp',
    create_fallback=True
)

STATIC_DIR = set_path(
    path=getenv('GALETTE_STATIC_DIR'),
    fallback='static',
)
    
TEMPLATES_DIR = set_path(
    path=getenv('GALETTE_TEMPLATES_DIR'),
    fallback='templates'
)

BUILD_DIR = set_path(
    path=getenv('GALETTE_BUILD_DIR'),
    fallback='.build',
    create_fallback=True
)