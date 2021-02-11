import os
from .base import *

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]

DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
