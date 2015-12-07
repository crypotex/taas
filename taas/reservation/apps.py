import django.apps

from django.db.models import signals as db_signals
from django.utils.translation import ugettext_lazy as _

from taas.reservation import handlers


class ReservationConfig(django.apps.AppConfig):
    name = 'taas.reservation'
    verbose_name = _('Reservation')

    def ready(self):
        Reservation = self.get_model('Reservation')

        db_signals.pre_delete.connect(
            handlers.delete_payment_before_last_reservation_delete,
            sender=Reservation,
            dispatch_uid='taas.reservation.handlers.delete_payment_before_last_reservation_delete',
        )
