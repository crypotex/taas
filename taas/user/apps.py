import django.apps
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _

from . import handlers


class UserConfig(django.apps.AppConfig):
    name = 'taas.user'
    verbose_name = _('User')

    def ready(self):
        User = self.get_model('User')

        signals.post_save.connect(
            handlers.send_emails_to_users,
            sender=User,
            dispatch_uid='user.handlers.send_emails_to_users',
        )

        signals.pre_save.connect(
            handlers.preserve_fields_before_update,
            sender=User,
            dispatch_uid='user.handlers.preserve_fields_before_update',
        )
