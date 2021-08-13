"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
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
    'api.logger.apps.LoggerConfig',
    'api.user.apps.UserConfig',
    'api.magazine.apps.MagazineConfig',
    'api.firebase.apps.FirebaseConfig',
    'api.commerce.cart.apps.CartConfig',
    'api.commerce.collection.apps.CollectionConfig',
    'api.commerce.coupon.apps.CouponConfig',
    'api.commerce.customer.apps.CustomerConfig',
    'api.commerce.order.apps.OrderConfig',
    'api.commerce.payment.apps.PaymentConfig',
    'api.commerce.product.apps.ProductConfig',
    'api.commerce.review.apps.ReviewConfig',
    'api.commerce.shipping.apps.ShippingConfig',
    'api.commerce.vendor.apps.VendorConfig',
    'api.commerce.wishlist.apps.WishlistConfig',
    ]

THIRD_PARTY_APPS = [
    'django_crontab',
    'rest_framework',
    'drf_yasg',
    'storages',
    'django_summernote',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.apple',
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

SITE_NAME = 'around-us'

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
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}


# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
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
CRONJOBS = [
    # ['* * * * *', 'api.cron.mall.create_tester'],
]

# SUMMERNOTE
SUMMERNOTE_CONFIG = {
    'attachment_model': 'magazine.Summernote',
    'iframe': True,
}
X_FRAME_OPTIONS = 'SAMEORIGIN'

# COOLSMS
COOLSMS_API_KEY = 'NCSMVIWDWDVLDXLG'
COOLSMS_API_SECRET = 'N9KGGSNNCBONQZAYKEP8QDIMPBISY8PS'
COOLSMS_FROM_PHONE = '01050319504'

# MAILGUN
MAILGUN_API_KEY = "a1209bfad6ca285a9ad2e0d7c1356b80-a0cfb957-2866bfcd"
MAILGUN_DOMAIN = "https://api.mailgun.net/v3/mail.dev-change.net"
MAILGUN_FROM_EMAIL = 'sofaissofa@icloud.com'

# CLAYFUL
CLAYFUL_API_KEY = '521bf375f86c91e5b9053b1fd461dddfc97bf568bfb056e8d26471febdd698ecee7e55f1'
CLAYFUL_API_SECRET = 'cab48c9b28a1fd40b8cb0dd38323f12716f4d00896c8e05476993676ef98b7fb7dfedad2f44b29b82705bf3650852cc3'

# SOCIAL REDIRECT URL
SOCIAL_REDIRECT_URL = 'http://localhost:8000/login/social/callback'
KAKAO_REDIRECT_URL = 'http://localhost:8000/accounts/kakao/login/callback/'

# KAKAO
KAKAO_CLIENT_ID = '834031fe8f729b4ce1c4d1865bccd63a'
KAKAO_CLIENT_SECRET = 'ArCJdOXV5GszOyZUj6WOqliE8bJ4DfUB'
KAKAO_LOGIN_URL = f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={KAKAO_CLIENT_ID}&redirect_uri={SOCIAL_REDIRECT_URL}&state=kakao'


# # APPLE
# APPLE_CLIENT_ID = '123'
# APPLE_CLIENT_SECRET = ''
#
# '''
# APPLE LOGIN URL
# https://appleid.apple.com/auth/authorize?response_type=code&client_id=${APPLE_CLIENT_ID}&redirect_uri={SOCIAL_REDIRECT_URL}&state=apple
# https://appleid.apple.com/auth/authorize?response_type=code&client_id=123&redirect_uri=http://localhost:3000/login/social/callback&state=apple
# '''