from django.test import TestCase
from freezegun import freeze_time
import json

from taas.reservation.tests.factories import ReservationFactory, FieldFactory
from taas.user.tests.factories import UserFactory
from taas.reservation.models import Reservation, Field
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta


class ReservationTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.field = FieldFactory()
        self.login_data = {'username': self.user.email, 'password': 'isherenow'}
        self.reservation_url = ReservationFactory.get_reservation_url()
        self.remove_url = ReservationFactory.get_remove_url()
        self.remove_all_url = ReservationFactory.get_remove_all_url()
        self.payment_url = ReservationFactory.get_reservation_list_url()
        self.all_reservations_url = ReservationFactory.get_all_reservations_url()
        self.reservation_list_url = ReservationFactory.get_reservation_list_url()

    @freeze_time("2015-11-11 17:00:00")
    def test_freezegun_datetime_now(self):
        self.assertEqual(datetime.now(), datetime.strptime("2015-11-11 17:00:00", '%Y-%m-%d %H:%M:%S'),
                         'freeze_time package might be not installed. datetime.now() should return 2015-11-11 17:00:00')

    def test_anon_user_cannot_add_reservation(self):
        response = self.client.get(self.reservation_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/add/'))

    def test_user_can_make_valid_reservation(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(10, 1)
        self._ensure_user_can_create_reservation(start, end, self.field)

    def test_user_can_make_multiple_reservations(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(10, 1)
        self._ensure_user_can_create_reservation(start, end, self.field)
        field2, field3 = FieldFactory.create_batch(2)
        self._ensure_user_can_create_reservation(start, end, field2)
        done_reservations = Reservation.objects.all().filter(start=start)
        self.assertEqual(done_reservations.count(), 2,
                         _('User should be able to make 2 reservations on same datetime on different fields'))
        self._ensure_user_can_create_reservation(start, end, field3)
        done_reservations = Reservation.objects.all().filter(start=start)
        self.assertEqual(done_reservations.count(), 3,
                         _('User should be able to make 2 reservations on same datetime on different fields'))

    def test_user_can_see_multiple_unpaid_reservations(self):
        ReservationFactory.create_batch(3, user=self.user)
        self.client.login(**self.login_data)
        response = self.client.get(ReservationFactory.get_reservation_list_url(),
                                   {'start': timezone.now().date(), 'end': timezone.now().date()})
        reservations = [reserv for reserv in response.context_data['table'].data]
        self.assertEqual(len(reservations), 3, _("All three reservations are shown"))

    def test_all_users_unpaid_reservations_are_deleted(self):
        self.client.login(**self.login_data)
        ReservationFactory.create_batch(3, user=self.user)
        self.client.post(self.remove_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(Reservation.objects.all().count(), 0,
                         _("Not all unpaid reservations are deleted"))

    def test_one_unpaid_reservation_can_be_deleted(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(10, 1)
        res_to_del = ReservationFactory(start=start, end=end, user=self.user)
        self.client.post(self.remove_url, {'id': str(res_to_del.id)}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(Reservation.objects.all().count(), 0, _("Unpaid Resevation is not deleted."))

    def test_reservation_is_not_paid_after_it_is_made(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(12, 5)
        self._ensure_user_can_create_reservation(start, end, self.field)
        done_reservations = Reservation.objects.all().filter(start=start)
        self.assertFalse(done_reservations[0].paid,
                         _("Reservation is automatically paid. It should be unpaid."))

    def test_anon_user_cannot_post_reservation(self):
        start, end = self.get_valid_datetime(12, 5)
        res_d = {'start': start, 'end': end, 'field': 'A'}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(len(Reservation.objects.all()), 0, _("Anonymous user can make a valid reservation"))
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/add/'))

    def test_user_cannot_post_reservation_with_missing_field_end(self):
        self.client.login(**self.login_data)
        res_d = {}
        start, end = self.get_valid_datetime(10, 10)
        res_d['start'] = start
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_end(self):
        self.client.login(**self.login_data)
        res_d = {}
        start, end = self.get_valid_datetime(10, 10)
        res_d['start'] = start
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_field(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(10, 10)
        res_d = {'start': start, 'end': end}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_data(self):
        self.client.login(**self.login_data)
        res_d = {}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_past_date(self):
        self.client.login(**self.login_data)
        start, end = self.get_valid_datetime(12, -10)
        res_d = {'start': start, 'end': end, 'field': 'A'}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_14_min_59_sec_before(self):
        self.client.login(**self.login_data)
        res_d = {}
        d = datetime.now()
        start = datetime(year=d.year, month=d.month, day=d.day, hour=17, minute=0, second=0)
        end = datetime(year=d.year, month=d.month, day=d.day, hour=18, minute=0, second=0)
        start, end = start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 15 minutes before"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted 15 minutes before"))

    @freeze_time("2015-11-11 17:5:00")
    def test_user_cannot_post_reservation_5_min_later(self):
        self.client.login(**self.login_data)
        res_d = {}
        d = datetime.now()
        start = datetime(year=d.year, month=d.month, day=d.day, hour=17, minute=0, second=0)
        end = datetime(year=d.year, month=d.month, day=d.day, hour=18, minute=0, second=0)
        start, end = start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 5 minutes after"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted 5 minutes after"))

    @freeze_time("2015-11-11 17:00:00")
    def test_user_cannot_post_reservation_0_min_0_sec_before(self):
        self.client.login(**self.login_data)
        res_d = {}
        start = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        end = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted at the same time of now()"))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted at the same time of now()"))

    @freeze_time("2015-11-11 17:01:00")
    def test_user_cannot_post_reservation_kala_min_before(self):
        self.client.login(**self.login_data)
        res_d = {}
        start = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        end = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 1 minute after "))
        self.assertEqual(len(Reservation.objects.all()), 0, _("Reservation posted at the same time of now()"))

    def _ensure_user_can_create_reservation(self, start, end, field):
        reservation_data = {'start': start, 'end': end, 'field': field.name}
        self.client.post(self.reservation_url, reservation_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        done_reservations = Reservation.objects.filter(start=start, field=field)
        self.assertTrue(done_reservations.exists(), _('No reservation made with valid data'))

    def get_valid_datetime(self, hour, days=0, minute=0, second=0):
        d = timezone.now() + timedelta(days=days)
        start = timezone.datetime(year=d.year, month=d.month, day=d.day, hour=hour,
                                  minute=minute, second=second)
        end = start + timedelta(hours=hour+1)
        return start.strftime("%Y-%m-%d %H:%M"), end.strftime("%Y-%m-%d %H:%M")

    def test_anon_user_cannot_removeall_reservations(self):
        response = self.client.post(self.remove_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/remove/all/'))

    def test_anon_user_cannot_remove_specific_reservation(self):
        response = self.client.post(self.remove_url, {'id': str(1)}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/remove/'))
