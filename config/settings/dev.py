from .base import *
import pymysql
import os

pymysql.install_as_MySQLdb()
DEBUG = True
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['*']

DB = 'mysql'

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
            'NAME': 'ustainrds',
            'USER': 'ustainrds',
            'PASSWORD': 'ustainrds123!',
            'HOST': 'ustainrds.cmhvcwhk2b1g.ap-northeast-2.rds.amazonaws.com',
            'PORT': '3306',
        }
    }


# S3
USE_S3 = True

if USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIAFILES_LOCATION = 'media'

AWS_S3_SECURE_URLS = True
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'ustain'
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION
AWS_ACCESS_KEY_ID = 'AKIAXN52GQSMTVQUMH63'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}