"""
Base settings for TAAS project
"""

import os

from django.conf import global_settings
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django_admin_bootstrapped',
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
        'anonymous': '#FE9900',
        'others': '#FE9900',
        'owner': '#008a00'
    },
    'unpaid': {
        'owner': '#8f62bd',
        'others': '#a9a9a9',
    },
    'update': '#A52A2A'
}

MAKSEKESKUS = {
    'publishable_key': '',
    'secret_key': '',
    'shop_id': '',
    'host': '',
    'locale': 'ee',
    'country': 'ee',
    'currency': 'EUR'
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

LANGUAGES = (
  ('et', _('Estonian')),
  ('en', _('English')),
  ('ru', _('Russian')),
)

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

FORMAT_MODULE_PATH = 'taas.formats'

TIME_FORMAT = 'H:i'
SHORT_DATETIME_FORMAT = 'd.m.Y H:i'
DATETIME_FORMAT = 'd.m.Y H:i'
