from .base import *
import pymysql
import os

pymysql.install_as_MySQLdb()
DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['*']

DB = 'sqlite'

if DB == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

if DB == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'change_dev',
            'USER': 'change_admin',
            'PASSWORD': 'change123!',
            'HOST': 'change-dev.cafpqcrl5o17.ap-northeast-2.rds.amazonaws.com',
            'PORT': '3306',
        }
    }

# S3
USE_S3 = False

if USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIAFILES_LOCATION = 'media'

AWS_S3_SECURE_URLS = True
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'changes3'
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION
AWS_ACCESS_KEY_ID = 'AKIATG64CU4RXKUKGP6P'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
