"""
Base settings for TAAS project
"""

import os

from django.conf import global_settings
from django.core.urlresolvers import reverse_lazy

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_tables2',
    'widget_tweaks',

    'taas.user',
    'taas.reservation',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = global_settings.TEMPLATE_LOADERS + (
    'django.template.loaders.eggs.Loader',
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
    os.path.join(PROJECT_ROOT, 'taas', 'templates'),
    os.path.join(PROJECT_ROOT, 'taas', 'user', 'templates'),
    os.path.join(PROJECT_ROOT, 'taas', 'reservation', 'templates'),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, 'locale'),
)

COLORS = {
    'paid': {
        'anonymous': '#4682B4',
        'others': '#7B68EE',
        'owner': '#483D8B'
    },
    'unpaid': {
        'owner': '#008000',
        'others': '#FF8C00',
    },
    'update': '#A52A2A'
}

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

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'taas', 'static'),
    os.path.join(PROJECT_ROOT, 'taas', 'user', 'static'),
    os.path.join(PROJECT_ROOT, 'taas', 'reservation', 'static'),
)

LOGIN_REDIRECT_URL = reverse_lazy('homepage')
LOGIN_URL = reverse_lazy('user_login_form')
