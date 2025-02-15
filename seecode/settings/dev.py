"""
Django settings for soc_web project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '\x97{\xfd\xcc\n1\xc15\x15,jO\xaf7xf8\x93\xb3\xebi)\xfdk\x8a\x05\xdd\x85%\xc4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cas.middleware.CASMiddleware',

]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cas',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',

    'debug_toolbar',
    'corsheaders',
    'django_celery_beat',

    'seecode.apps.api.v2',
    'seecode.apps.project',
    'seecode.apps.node',
    'seecode.apps.authenticate',
    'seecode.apps.system',
    'seecode.apps.tactic',
    'seecode.apps.scan',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],

        'APP_DIRS': True,
        'OPTIONS': {
            "debug": DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'seecode.apps.system.views.base.permission_settings',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

ROOT_URLCONF = 'seecode.urls'
WSGI_APPLICATION = 'seecode.wsgi.application'
LOGIN_URL = '/login'
PROXY_DOMAIN = 'http://127.0.0.1:8080'

ENABLE_CAS_SSO = False
CAS_SERVER_URL = "http://sso.example.com/"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'seecode_db_ce',  # Or path to database file if using sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': '',
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'charset': 'utf8mb4'}
    }

}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "KEY_PREFIX": "seecode_ce",
        "LOCATION": "redis://127.0.0.1:6379/7",
        "OPTIONS": {
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            "SOCKET_TIMEOUT": 5,  # in seconds
            "PICKLE_VERSION": -1  # Use the latest protocol version
        }
    }
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
CACHE_PAGE_TIMEOUT = 60 * 1

CORS_ORIGIN_WHITELIST = (
    'http://localhost',
    'http://127.0.0.1',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
UPLOAD_URL = '/media/upload/'
UPLOAD_ROOT = os.path.join(MEDIA_ROOT, 'upload')
UPGRADE_ROOT = os.path.join(MEDIA_ROOT, 'upgrade')

# Alarm
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.protonmail.com'
EMAIL_HOST_USER = 'alarm@protonmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

# CELERY
CELERY_BROKER_URL = "redis://127.0.0.1:6379/7"
