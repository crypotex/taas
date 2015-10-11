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
        data = {'date' : '2015-11-11',
                'timeslot' : '18',
                'fields' : '1',
                'method' : '1',}
        return data

    def test_freezegun_datetime_now(self):
        self.assertEqual(datetime.now(), datetime.strptime("2015-11-11 17:00:00", '%Y-%m-%d %H:%M:%S'),
                         'freeze_time package might be not installed. datetime.now() should return 2015-11-11 17:00:00')

    def log_in(self):
        return self.client.login(username=self.user.email, password='isherenow', follow=True)

    def test_logged_in_user_can_access_reservation_page(self):
        response = self.log_in()
        self.assertEqual(response.status_code, http_client.OK)

    def test_anon_user_cannot_access_reservation_page(self):
        response = self.client.get(self.reservation_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/make/'))

    def test_auth_user_cannot_create_reservation_without_date(self):
        response = self.log_in()
        self.reservation['date'] = ''
        self.assertRaises(KeyError, lambda: self.client.post(self.reservation_url, self.reservation))

    def test_auth_user_cannot_create_reservation_without_timeslot(self):
        response = self.log_in()
        self.reservation['timeslot'] = ''
        self.assertRaises(KeyError, lambda: self.client.post(self.reservation_url, self.reservation))

    def test_auth_user_cannot_create_reservation_with_past_date(self):
        response = self.log_in()
        self.reservation['date'] = '2015-10-10'
        response = self.client.post(self.reservation_url, self.reservation)
        done_reservations = Reservation.objects.all().filter(date='2015-10-10')
        self.assertFalse(done_reservations, _('Reservation was made with invalid date'))
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made with invalid date'))

    def test_auth_user_cannot_create_reservation_with_past_timeslot(self):
        response = self.log_in()
        self.reservation['timeslot'] = '11'
        response = self.client.post(self.reservation_url, self.reservation)
        done_reservations = Reservation.objects.all().filter(date='2015-11-11', timeslot='11')
        self.assertFalse(done_reservations, _('Reservation was made with invalid timeslot'))
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made with invalid timeslot'))

    @freeze_time("2015-11-11 17:31:00")
    def test_user_cannot_create_reservation_29_minutes_before(self):
        response = self.log_in()
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made 29 minutes before'))
        done_reservations = Reservation.objects.all().filter(date=self.reservation['date'], timeslot=self.reservation['timeslot'])
        self.assertEqual(done_reservations.count(), 0, msg=_('Reservation was made 29 minutes before'))

    def test_reservation_cannot_be_made_to_right_now(self):
        response = self.log_in()
        self.reservation['timeslot'] = '17'
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made for right now'))
        done_reservations = Reservation.objects.all().filter(date=self.reservation['date'], timeslot='17')
        self.assertEqual(done_reservations.count(), 0, msg=_('Reservation was made for right now'))

    @freeze_time("2015-11-11 17:25:00")
    def test_user_cannot_make_reservation_25_min_later(self):
        response = self.log_in()
        self.reservation['timeslot'] = '17'
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made for right now'))
        done_reservations = Reservation.objects.all().filter(date=self.reservation['date'], timeslot='17')
        self.assertEqual(done_reservations.count(), 0, msg=_('Reservation was made for right now'))

    @freeze_time("2015-11-11 17:35:00")
    def test_user_cannot_make_reservation_35_min_later(self):
        response = self.log_in()
        self.reservation['timeslot'] = '17'
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Reservation was made for right now'))
        done_reservations = Reservation.objects.all().filter(date=self.reservation['date'], timeslot='17')
        self.assertEqual(done_reservations.count(), 0, msg=_('Reservation was made for right now'))

    def test_auth_user_cannot_create_duplicate_reservations(self):
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', '1', 1)
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Duplicate reservations happened.'))
        done_reservations = Reservation.objects.all().filter(date='2015-11-11', timeslot='18')
        self.assertTrue(done_reservations.count()==1, _('Duplicate reservations happened'))

    def test_user_can_book_all_three_fields(self):
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', ['1','2','3'], 1)
        self.assertEqual(Reservation.objects.get(date='2015-11-11', timeslot='18').fields.count(), 3,
                         _('There are different amount of fields booked - wrongly made valid reservation'))

    def test_user_can_create__three_reservations_on_same_timeslot(self):
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', '1', 1)
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', '2', 2)
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', '3', 3)

    def test_user_cannot_create_partial_reservation(self):
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', ['1','2'], 1)
        self.reservation['fields'] = ['2','3']
        response = self.client.post(self.reservation_url, self.reservation)
        self.assertEqual(http_client.OK, response.status_code, _('Duplicate reservations happened'))
        done_reservations = Reservation.objects.all().filter(date=self.reservation['date'], timeslot=self.reservation['timeslot'])
        self.assertTrue(done_reservations.count()==1, _('Duplicate reservations happened'))

    def test_user_can_make_valid_reservation(self):
        response = self.post_valid_reservation(self.reservation, '2015-11-11', '18', '1', 1)

    def post_valid_reservation(self, reservation_data, date_string, timeslot, fields, how_many_fields):
        response = self.log_in()
        reservation_data['fields'] = fields
        reservation_data['date'] = date_string
        reservation_data['timeslot'] = timeslot
        response = self.client.post(self.reservation_url, reservation_data)
        self.assertRedirects(response, reverse('homepage'))
        done_reservations = Reservation.objects.all().filter(date=date_string, timeslot=timeslot)
        self.assertTrue(done_reservations.count() == how_many_fields, _('No reservation made with valid data'))
        return response