from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'myanimals.sqlite3',
    }
}

CORS_ORIGIN_ALLOW_ALL = True