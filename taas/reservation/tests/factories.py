import datetime

from django.core.urlresolvers import reverse

import factory
import factory.fuzzy

from taas.reservation.models import Field, Reservation
from taas.user.tests.factories import UserFactory


class FieldFactory(factory.DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Iterator(['A', 'B', 'C'])
    cost = factory.fuzzy.FuzzyFloat(5, 30)
    description = factory.Sequence(lambda n: 'Description %s' % n)


class ReservationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reservation

    date = datetime.datetime.strptime('2015-11-11', '%Y-%m-%d').date()
    timeslot = "19"
    user = factory.SubFactory(UserFactory, is_active=True)
    method = factory.fuzzy.FuzzyChoice([1, 2])

    @factory.post_generation
    def fields(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for field in extracted:
                self.fields.add(field)

    @classmethod
    def get_reservation_url(cls):
        return 'http://testserver' + reverse('add_reservation')
