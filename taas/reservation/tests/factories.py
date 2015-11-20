import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone

import factory
import factory.fuzzy

from taas.reservation.models import Field, Reservation, Payment
from taas.user.tests.factories import UserFactory


class FieldFactory(factory.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Sequence(lambda n: 'Field {0}'.format(n))
    cost = factory.fuzzy.FuzzyDecimal(5, 30)
    description = factory.Sequence(lambda n: 'Description %s' % n)


class ReservationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reservation

    start = factory.fuzzy.BaseFuzzyDateTime(start_dt=timezone.now() + datetime.timedelta(days=1),
                                            end_dt=timezone.now() + datetime.timedelta(days=2), force_hour=12)
    end = factory.LazyAttribute(lambda o: o.start + datetime.timedelta(hours=1))
    user = factory.SubFactory(UserFactory, is_active=True)
    field = factory.SubFactory(FieldFactory)

    @classmethod
    def get_reservation_url(cls):
        return 'http://testserver' + reverse('add_reservation')

    @classmethod
    def get_remove_url(cls):
        return 'http://testserver' + reverse('remove_reservation')

    @classmethod
    def get_remove_all_url(cls):
        return 'http://testserver' + reverse('remove_all_reservations')

    @classmethod
    def get_reservation_list_url(cls):
        return 'http://testserver' + reverse('reservation_list')

    @classmethod
    def get_all_reservations_url(cls):
        return 'http://testserver' + reverse('all_reservations')

    @classmethod
    def get_reservation_list_url(cls):
        return 'http://testserver' + reverse('reservation_list')

    @classmethod
    def get_expire_url(cls):
        return 'http://testserver' + reverse('get_expire_time')

    @classmethod
    def get_reservation_history_url(cls):
        return 'http://testserver' + reverse('reservation_history')

    @classmethod
    def get_reservation_detail_url(cls, pk):
        return 'http://testserver' + reverse('detail_reservation', kwargs={'pk': pk})


class PaymentFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Payment

    amount = factory.fuzzy.FuzzyDecimal(0.0)
    user = factory.SubFactory(UserFactory)
    type = factory.fuzzy.FuzzyChoice([Payment.BUDGET, Payment.TRANSACTION])

    @classmethod
    def get_payment_success_url(cls):
        return 'http://testserver' + reverse('payment_success')

    @classmethod
    def get_payment_cancel_url(cls):
        return 'http://testserver' + reverse('payment_cancel')

    @classmethod
    def get_budget_payment_url(cls):
        return 'http://testserver' + reverse('budget_payment')
