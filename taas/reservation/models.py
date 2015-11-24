from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taas.user.models import User


class Field(models.Model):
    name = models.CharField(_('name'), max_length=10, unique=True)
    cost = models.DecimalField(_('cost'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('field')
        verbose_name_plural = _('fields')


class Payment(models.Model):
    TRANSACTION = 'TR'
    BUDGET = 'BU'
    STAGED = 'ST'
    PAYMENT_CHOICES = (
        (TRANSACTION, _('Transaction')),
        (BUDGET, _('Budget')),
        (STAGED, _('Staged')),
    )

    type = models.CharField(choices=PAYMENT_CHOICES, max_length=2, verbose_name=_('type'))
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    user = models.ForeignKey(User, verbose_name=_('user'))

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __str__(self):
        return str(self.pk)


class Reservation(models.Model):
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))
    user = models.ForeignKey(User, limit_choices_to={'is_active': True}, related_name="reservations",
                             verbose_name=_('user'))
    field = models.ForeignKey(Field, related_name="reservations",
                              verbose_name=_('field'))
    paid = models.BooleanField(_('Paid'), default=False)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)
    payment = models.ForeignKey(Payment, verbose_name=_('Payment'), blank=True,
                                null=True, on_delete=models.SET_NULL)

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
        tzdt = timezone.datetime.today()
        startdt = self.get_start()
        return tzdt.year <= startdt.year and tzdt.month <= startdt.month and tzdt.day < self.get_start().day

    def can_update(self):
        if not self.paid:
            return False

        # It should be possible to update reservation 15 minutes before start.
        diff = self.get_start() - timezone.now()
        tzdt = timezone.datetime.today()
        startdt = self.get_start()
        return tzdt.year <= startdt.year and tzdt.month <= startdt.month and tzdt.day <= startdt.day and \
               divmod(diff.days * 86400 + diff.seconds, 60)[0] > 15
