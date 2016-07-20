from malanimals.settings import *
import dj_database_url
import os

DATABASES['default']['CONN_MAX_AGE'] = 500
DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

ALLOWED_HOSTS = [".herokuapp.com"]
