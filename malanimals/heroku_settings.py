from malanimals.settings import *
import dj_database_url
import os

DATABASES['default']['CONN_MAX_AGE'] = 500
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True
AWS_S3_FILE_OVERWRITE = True
AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_S3_SECURE_URLS = False
AWS_HEADERS = {
    'Cache-Control': 'max-age=31536000',
    'Vary': 'Accept-Encoding',
}

DEFAULT_FILE_STORAGE = 'malanimals.s3utils.MediaS3BotoStorage'
STATICFILES_STORAGE = 'malanimals.s3utils.OptimizedS3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + 'static/'
STATIC_ROOT = STATIC_URL
MEDIA_URL = S3_URL + 'media/'
MEDIA_ROOT = MEDIA_URL

DEBUG = False

TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

ALLOWED_HOSTS = [".herokuapp.com"]
