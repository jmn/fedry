"""
Django settings for dj project.

Generated by 'django-admin startproject' using Django 1.11.4.
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
SECRET_KEY = 'z41==&_v&t7zop!0ic6j8j#460iqwjbo50^v-s$6s-#_=i*zpg'
DEBUG = True
ALLOWED_HOSTS = ['*'] # Heroku

# Application definition
INSTALLED_APPS = [
    'djstripe',
    'corsheaders',
    'django_rq',
    'el_pagination',
    'fontawesome',
    'tagulous',
    'fd',
    'sn',
#    'oauth',
#    'silk',
    'analytical',
    'feeds',
    'django_bleach',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'bootstrap4',
    'social_django',
    'debug_toolbar',
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
#    'silk.middleware.SilkyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'fd.utils.AuthRequiredMiddleware',
#    'djstripe.middleware.SubscriptionPaymentMiddleware',

]

ROOT_URLCONF = 'dj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['fd/templates', 'sn/templates', 'dj/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]

WSGI_APPLICATION = 'dj.wsgi.application'

DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='postgres://postgres:aoeuaoeu@localhost:5432/fedry')
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = '/home/fedry/static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_DIRS = (BASE_DIR, 'static')

STATICFILES_DIRS = (                                                                 
 os.path.join(BASE_DIR, 'static/'),                                                
 BASE_DIR                                                                          
)             
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
SOCIAL_AUTH_GITHUB_KEY = '38f135c8216782fed0b3'
SOCIAL_AUTH_GITHUB_SECRET = 'f086fc11dee76ff7931ec72087b8d24ea3408ac3'
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '468496975653-34s4ehtap3k2308cup7062nfsuqie0jd.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Gdv_G4PQSW_gqpnZlhplggD-'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'https://www.fedry.net/'
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
BLEACH_STRIP_TAGS = True
BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a','pre','code','ul','li','h1','h2','h3','h4','h5','blockquote','span','div','table','th','tr','td','thead','tbody','img','aside','ol','dl','dt','dd','sup','br','kbd']
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style','src','width','height']
FONTAWESOME_CSS_URL = '//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
}


BOOTSTRAP4 = {
    'css_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css',
    'include_jquery' : True,
}

RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    }
}

CORS_ORIGIN_WHITELIST = (
    'localhost:8001',
    'localhost:8000',
)

GOOGLE_ANALYTICS_PROPERTY_ID =  'UA-106346242-1'

STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "pk_live_2YQdqgsd3JtquaX12gBIsj4O")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "sk_live_GWARAotxGXtZoeTJeLO8TIUl")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_dZCQLCB9Cn1RlBM63vuy3GFg")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_b4ElgT3Wx6vorW3zegyuxRIh")
STRIPE_LIVE_MODE = True

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://aeee2caa798c4fb5beeee4d18be9ff7c@sentry.io/1316090",
    integrations=[DjangoIntegration()]
)

INTERNAL_IPS = ['127.0.0.1', '81.226.138.87']
