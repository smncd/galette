from os import getenv
from galette.utils import set_path

DEBUG = getenv('DEBUG', False) in ('true', '1')

PAGES_DIR = set_path(getenv('PAGES_DIR', '/pages'))
ASSETS_DIR = set_path(getenv('ASSETS_DIR', '/assets'))

STATIC_DIR = set_path(
    path=getenv('STATIC_DIR', '/static'),
    fallback='static',
)
    
TEMPLATES_DIR = set_path(
    path=getenv('TEMPLATES_DIR', '/templates'),
    fallback='templates'
)
