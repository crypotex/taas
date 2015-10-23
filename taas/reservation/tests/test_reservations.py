from django.core.urlresolvers import reverse
from django.test import TestCase

from taas.reservation.tests.factories import ReservationFactory, FieldFactory
from taas.user.tests.factories import UserFactory
from taas.reservation.models import Reservation
from freezegun import freeze_time
from http import client as http_client
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

@freeze_time("2015-11-11 17:00:00")
class ReservationTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.fields = FieldFactory.create_batch(3)
        self.reservation = self.get_reservation_data()
        self.login_data = {'username': self.user.email, 'password': 'isherenow'}
        self.login_url = UserFactory.get_login_url()
        self.reservation_url = ReservationFactory.get_reservation_url()

    def get_reservation_data(self):
        data = {'start' : '2015-11-11',
                'end' : '18',
                'fields' : 'A',}
        return data

    def test_freezegun_datetime_now(self):
        self.assertEqual(datetime.now(), datetime.strptime("2015-11-11 17:00:00", '%Y-%m-%d %H:%M:%S'),
                         'freeze_time package might be not installed. datetime.now() should return 2015-11-11 17:00:00')

    def log_in(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertRedirects(response,
                             expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk,
                         'User cannot login with valid data.')

    def test_anon_user_cannot_add_reservation(self):
        response = self.client.get(self.reservation_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/add/'))

    def test_user_can_make_valid_reservation(self):
        response = self.log_in()
        response = self.post_valid_reservation('2015-10-23 20:00:00+03:00', '2015-10-23 21:00:00+03:00', 'A', 1)

    def post_valid_reservation(self, start, end, field, how_many_fields):
        reservation_data = {}
        reservation_data['field'] = field
        reservation_data['start'] = start
        reservation_data['end'] = end
        response = self.client.post(self.reservation_url, reservation_data)
        print(response.status_code)
        #self.assertRedirects(response, reverse('homepage'))
        done_reservations = Reservation.objects.all()
        print(done_reservations)
        #self.assertTrue(done_reservations.count() == how_many_fields, _('No reservation made with valid data'))
        return response