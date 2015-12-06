from taas.server.base_settings import *
from taas.server.email_settings import *

SECRET_KEY = 'test-key'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

CELERYBEAT_SCHEDULE = {
    'remove-expired-reservations': {
        'task': 'taas.reservation.tasks.remove_expired_reservations',
        'schedule': timedelta(minutes=5),
    },
}

EMAIL_HOST = 'smtp.example.com'

EMAIL_HOST_USER = 'test.user@example.com'

EMAIL_HOST_PASSWORD = 'test'

ADMIN_EMAILS = ['test.admin@example.com']

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(PROJECT_ROOT, 'inbox')
