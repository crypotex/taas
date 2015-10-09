import django.apps
from django.contrib.auth import signals as auth_signals
from django.db.models import signals as db_signals
from django.utils.translation import ugettext_lazy as _

from taas.user import handlers


class UserConfig(django.apps.AppConfig):
    name = 'taas.user'
    verbose_name = _('User')

    def ready(self):
        User = self.get_model('User')

        db_signals.post_save.connect(
            handlers.send_emails_to_users,
            sender=User,
            dispatch_uid='taas.user.handlers.send_emails_to_users',
        )

        auth_signals.user_logged_in.connect(
            handlers.log_user_login,
            sender=User,
            dispatch_uid='taas.user.handlers.log_user_login'
        )

        auth_signals.user_logged_out.connect(
            handlers.log_user_logout,
            sender=User,
            dispatch_uid='taas.user.handlers.log_user_logout'
        )

        auth_signals.user_login_failed.connect(
            handlers.log_user_login_failed,
            dispatch_uid='taas.user.handlers.log_user_logout'
        )
