import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taas.user.models import User
from django.core.validators import MinValueValidator

# Create your models here.

logger = logging.getLogger(__name__)

'''
class ReservationManager:

    def calc_payment(self, fields):
        sum = 0
        for field in fields:
            sum += field.cost
        return sum

    def create_reservation(self, date, timeslot, fields, method, user, **extra_fields):
        now = timezone.now()
        reservation = self.model(
            date = date,
            timeslot = timeslot,
            fields = fields,
            method = method,
            user = user,
            **extra_fields
        )
        payment = self.calc_payment(fields)
        reservation.save(using=self._db)
        return reservation
    ## Have to add remove_sum_from_user also

    def multiple_reservations(self, in_data):
        for res in in_data:
            self.create_reservation(res[0], res[1], res[2], res[3], res[4], res[5:])

'''



class Field(models.Model):
    name = models.CharField(_('field'), max_length=1, unique=True)
    cost = models.FloatField(_('cost'), validators=[MinValueValidator(0.0)])
    description = models.TextField(_('description'))

PAYMENT_METHOD_CHOICES = (
    (1,_('Payment made with bank link.')),
    (2, _('Payment made with existing budget'))
)

class Reservation(models.Model):
    date = models.DateField(_('date'))
    timeslot = models.TimeField(_('timeslot'))
    user = models.ForeignKey(User, limit_choices_to={'is_active': True}, related_name="reservations")
    fields = models.ManyToManyField(Field)
    payment_sum = models.FloatField(_('payment sum'), validators=[MinValueValidator(0.0)])
    method = models.IntegerField(choices = PAYMENT_METHOD_CHOICES)
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    REQUIRED_FIELDS = ['date' , 'timeslot', 'user', 'fields', 'payment_sum', 'method', 'date_created']

    class Meta:
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')