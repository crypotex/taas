import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taas.user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

logger = logging.getLogger(__name__)

class Field(models.Model):
    name = models.CharField(_('field'), max_length=30, unique=True)
    cost = models.FloatField(_('cost'), validators=[MinValueValidator(0.0)])
    description = models.TextField(_('description'))

    def __str__(self):
        return self.name

PAYMENT_METHOD_CHOICES = (
    (1,_('Payment made with bank link.')),
    (2, _('Payment made with existing budget'))
)

class Reservation(models.Model):
    date = models.DateField(_('date'))
    timeslot = models.SmallIntegerField(_('timeslot'), validators=[MinValueValidator(8), MaxValueValidator(21)])
    user = models.ForeignKey(User, limit_choices_to={'is_active': True}, related_name="reservations")
    fields = models.ManyToManyField(Field)
    method = models.IntegerField(choices = PAYMENT_METHOD_CHOICES)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')

    def __str__(self):
        return str(self.pk)

    def _calc_payment_sum(self):
        sum = 0
        for field in self.fields.all():
            sum += field.cost
        return sum

    payment_sum = property(_calc_payment_sum)

