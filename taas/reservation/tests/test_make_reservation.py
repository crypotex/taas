from django.test import TestCase
from datetime import datetime
from freezegun import freeze_time
from taas.user.tests.factories import UserFactory
from taas.reservation.models import Reservation, Field
from django.core.urlresolvers import reverse
from django.http.request import QueryDict
from http import client

@freeze_time("2015-11-11 17:00:00")
class test_make_reservation(TestCase):

    def get_reservation_url(self):
        return 'http://testserver' + reverse('reservation_form')

    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.reservation = self.reservation_data(self.user)
        self.login_data = {'username': self.user.email, 'password': 'isherenow'}
        self.login_url = UserFactory.get_login_url()
        self.reservation_url = self.get_reservation_url()
        self.all_fields = self.make_fields()

    def reservation_data(self, user):
        data = QueryDict('', mutable=True)
        data.update({'date': '2015-11-11'})
        data.update({'timeslot': '18'})
        data.update({'method': '1'})
        data.update({'fields': '1'})
        data.update({'User': '1'})
        return data

    def test_freezegun_datetime_now(self):
        self.assertEqual(datetime.now(), datetime.strptime("2015-11-11 17:00:00", '%Y-%m-%d %H:%M:%S'),
                         'freeze_time package might be not installed. datetime.now() should return 2015-11-11 17:00:00')
    '''
    def logged_in_user_can_access_reservation_page(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)
        response = self.client.get(self.reservation_url)
        self.client.post(self.reservation)
    '''
    def make_fields(self):
        f1 = Field.objects.create(name='A', cost='5.0')
        f2 = Field.objects.create(name='B', cost='5.0')
        f3 = Field.objects.create(name='C', cost='5.0')
        f1.save()
        f2.save()
        f3.save()

    def reservation_with_valid_data_can_be_made(self):
        field = Field.objects.get(pk = 1)
        print(field)
        reservation = Reservation(date='2015-11-11', timeslot='18', method='1', user=self.user)
        reservation.save()
        reservation.fields.add(field)
        reservation.save()
        print(Reservation.objects.get(pk = 1).fields)
        #Reservation.objects.create(self.reservation)
