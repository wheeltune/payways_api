import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='b-eaqe=c(s79x1f+elyut9^_6xw8jmvz#^d76ot52r87e119j7')

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]

DEBUG = os.getenv('DJANGO_DEBUG', '1') == '1'
