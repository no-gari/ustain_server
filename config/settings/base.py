import datetime
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pj%2ze09(g)i^joilp-f8gvs)6ou_m036u3ejs^ky&9nse5k92'

ALLOWED_HOSTS = [
    '*.ap-northeast-2.elasticbeanstalk.com'
]

# SECURITY WARNING: don't run with debug turned on in production!


# Application definition
DJANGO_APPS = [
    'admin_menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

LOCAL_APPS = [
    'api.user.apps.UserConfig',
    'api.logger.apps.LoggerConfig',
    'api.mypage.apps.MypageConfig',
    'api.magazine.apps.MagazineConfig',
    # 'api.firebase.apps.FirebaseConfig',
    'api.commerce.cart.apps.CartConfig',
    'api.commerce.order.apps.OrderConfig',
    'api.commerce.review.apps.ReviewConfig',
    'api.commerce.search.apps.SearchConfig',
    'api.commerce.coupon.apps.CouponConfig',
    'api.commerce.comment.apps.CommentConfig',
    'api.commerce.product.apps.ProductConfig',
    'api.commerce.customer.apps.CustomerConfig',
    'api.commerce.collection.apps.CollectionConfig',
]

THIRD_PARTY_APPS = [
    'storages',
    'rest_framework',
    'drf_yasg',
    'django_summernote',
    'dj_rest_auth',
    'allauth',
]

SITE_ID = 1

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_NAME = 'ustain'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# AUTH_USER_MODEL
AUTH_USER_MODEL = 'user.User'

# APPLICATION
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'

# HOST
DEFAULT_HOST = 'api'
ROOT_HOSTCONF = 'config.hosts'
ROOT_URLCONF = 'config.urls.api'

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=8),
    'ROTATE_REFRESH_TOKENS': True,
}

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.user.serializers.login.CustomJWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DATETIME_FORMAT': '%Y.%m.%d',
}

# SWAGGER
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'config.swagger.SquadSwaggerAutoSchema',
    'USE_SESSION_AUTH': True,
    'DOC_EXPANSION': 'list',
    'APIS_SORTER': 'alpha',
    'SECURITY_DEFINITIONS': None,
    'DEFAULT_API_URL': 'http://127.0.0.1:8000/api/'
}

# CHANNELS
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# CRONTAB
# CRONJOBS = [
#     # ['* * * * *', 'api.cron.mall.create_tester'],
# ]

# SUMMERNOTE
SUMMERNOTE_CONFIG = {
    'attachment_model': 'magazine.Summernote',
    'iframe': True,
}
X_FRAME_OPTIONS = 'SAMEORIGIN'
