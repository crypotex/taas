"""
Base settings for TAAS project
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DEBUG = False
TEMPLATE_DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'taas.user',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'user', 'templates'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

ROOT_URLCONF = 'taas.urls'

AUTH_USER_MODEL = 'user.User'

WSGI_APPLICATION = 'taas.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Tallinn'

USE_I18N = True

USE_L10N = True

USE_TZ = True
