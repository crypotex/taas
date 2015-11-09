from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taas.user.models import User


class Field(models.Model):
    name = models.CharField(_('name'), max_length=10, unique=True)
    cost = models.DecimalField(_('cost'), max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

PAYMENT_METHOD_CHOICES = (
    (1, _('Payment made with bank link.')),
    (2, _('Payment made with existing budget'))
)


class Reservation(models.Model):
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))
    user = models.ForeignKey(User, limit_choices_to={'is_active': True}, related_name="reservations")
    field = models.ForeignKey(Field, related_name="reservations")
    paid = models.BooleanField(_('Paid'), default=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')

    def __str__(self):
        return str(self.pk)

    def _get_price(self):
        diff = (self.end - self.start).seconds / (60 * 60)

        return Decimal(diff) * self.field.cost

    price = property(_get_price)

    def get_start(self):
        return timezone.localtime(self.start)

    def get_end(self):
        return timezone.localtime(self.end)

    def get_date_created(self):
        return timezone.localtime(self.date_created)

    def can_delete(self):
        if not self.paid:
            return True

        # It should be possible to remove reservation before start day.
        return timezone.datetime.today().day < self.get_start().day

    def can_update(self):
        if not self.paid:
            return False

        # It should be possible to update reservation 15 minutes before start.
        diff = self.get_start() - timezone.now()
        return divmod(diff.days * 86400 + diff.seconds, 60)[0] > 15
