import os
os.environ["DJANGO_READ_DOT_ENV_FILE"] = "true"
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='b-eaqe=c(s79x1f+elyut9^_6xw8jmvz#^d76ot52r87e119j7')

CORS_ORIGIN_WHITELIST = (
    'localhost:3000/'
)

DEBUG = env.bool('DJANGO_DEBUG', default=True)
