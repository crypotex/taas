from django.core.urlresolvers import reverse
from django.test import TestCase

from taas.reservation.tests.factories import ReservationFactory, FieldFactory
from taas.user.tests.factories import UserFactory
from taas.reservation.models import Reservation, Field
from freezegun import freeze_time
from http import client as http_client
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

class ReservationTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.fields = FieldFactory.create_batch(3)
        self.login_data = {'username': self.user.email, 'password': 'isherenow'}
        self.login_url = UserFactory.get_login_url()
        self.reservation_url = ReservationFactory.get_reservation_url()
        self.remove_url = ReservationFactory.get_remove_url()
        self.remove_all_url = ReservationFactory.get_remove_all_url()
        self.payment_url = ReservationFactory.get_payment_url()
        self.all_reservations_url = ReservationFactory.get_all_reservations_url()
        self.reservation_list_url = ReservationFactory.get_reservation_list_url()

    @freeze_time("2015-11-11 17:00:00")
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
        self.log_in()
        start, end = self.get_valid_datetime(10, 1)
        self.post_valid_reservation(start, end, 'A')

    def test_user_can_make_multiple_reservations(self):
        self.log_in()
        start, end = self.get_valid_datetime(10,1)
        t_start, t_end = self.reformat_startend_timestring(start, end)
        self.post_valid_reservation(start, end, 'A')
        self.post_valid_reservation(start, end, 'B')
        done_reservations = Reservation.objects.all().filter(start = t_start, end = t_end)
        self.assertTrue(done_reservations.count() == 2,
                        _('User should be able to make 2 reservations on same datetime on different fields'))
        self.post_valid_reservation(start, end, 'C')
        done_reservations = Reservation.objects.all().filter(start = t_start, end = t_end)
        self.assertTrue(done_reservations.count() == 3,
                        _('User should be able to make 2 reservations on same datetime on different fields'))

    def test_user_can_see_multiple_unpaid_reservations(self):
        self.test_user_can_make_multiple_reservations()
        response = self.client.get(self.reservation_list_url, {'start': datetime.now().date(), 'end': datetime.now().date()})
        self.assertTrue(len(response.context_data['reservation_list']) == 3, _("All three reservations are shown"))

    def test_all_users_unpaid_reservations_are_deleted(self):
        self.test_user_can_make_multiple_reservations()
        self.client.post(self.remove_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertTrue(Reservation.objects.all().count() == 0,
                        _("Not all unpaid reservations are deleted"))

    def test_1_unpaid_reservation_can_be_deleted(self):
        self.log_in()
        start, end = self.get_valid_datetime(10, 1)
        for f in ('A', 'B'):
            self.post_valid_reservation(start, end, f)
        t_start, t_end = self.reformat_startend_timestring(start, end)
        field_id = Field.objects.all().filter(name = 'B')
        res_to_del = Reservation.objects.filter(start = t_start, end = t_end, field = field_id)[0].id
        self.client.post(self.remove_url, {'id':str(res_to_del)}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertTrue(Reservation.objects.all().count()==1, _("Unpaid Resevation is not deleted."))

    def test_reservation_is_not_paid_after_it_is_made(self):
        self.log_in()
        start, end = self.get_valid_datetime(12, 5)
        self.post_valid_reservation(start, end, 'A')
        t_start, t_end = self.reformat_startend_timestring(start, end)
        done_reservations = Reservation.objects.all().filter(start = t_start, end = t_end)
        self.assertTrue(done_reservations[0].paid == False, _("Reservation is automatically paid. It should be unpaid."))

    def test_anon_user_cannot_post_reservation(self):
        start, end = self.get_valid_datetime(12, 5)
        res_d = {'start': start, 'end': end, 'field':'A'}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertTrue(len(Reservation.objects.all()) == 0, _("Anonymous user can make a valid reservation"))
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/add/'))

    def test_user_cannot_post_reservation_with_missing_field_end(self):
        self.log_in()
        res_d = {}
        start, end = self.get_valid_datetime(10, 10)
        res_d['start'] = start
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_end(self):
        self.log_in()
        res_d = {}
        start, end = self.get_valid_datetime(10, 10)
        res_d['start'] = start
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_field(self):
        self.log_in()
        res_d = {}
        start, end = self.get_valid_datetime(10, 10)
        res_d['start'] = start
        res_d['end'] = end
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_missing_data(self):
        self.log_in()
        res_d = {}
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted with missing data"))

    def test_user_cannot_post_reservation_with_past_date(self):
        self.log_in()
        res_d = {}
        start, end = self.get_valid_datetime(12, -10)
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH = "XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted with missing data"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted with missing data"))

    @freeze_time("2015-11-11 16:45:01")
    def test_user_cannot_post_reservation_14_min_59_sec_before(self):
        self.log_in()
        res_d = {}
        d = datetime.now()
        start = datetime(year=d.year, month=d.month, day=d.day, hour=17, minute=0, second=0)
        end = datetime(year=d.year, month=d.month, day=d.day, hour=18, minute=0, second=0)
        start, end = start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH = "XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 15 minutes before"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted 15 minutes before"))

    @freeze_time("2015-11-11 17:5:00")
    def test_user_cannot_post_reservation_5_min_later(self):
        self.log_in()
        res_d = {}
        d = datetime.now()
        start = datetime(year=d.year, month=d.month, day=d.day, hour=17, minute=0, second=0)
        end = datetime(year=d.year, month=d.month, day=d.day, hour=18, minute=0, second=0)
        start, end = start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH = "XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 5 minutes after"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted 5 minutes after"))

    @freeze_time("2015-11-11 16:45:00")
    def test_user_can_make_reservation_15_minutes_before(self):
        self.log_in()
        start, end = self.get_valid_datetime(17)
        self.post_valid_reservation(start, end, 'A')

    @freeze_time("2015-11-11 16:44:55")
    def test_user_can_make_reservation_15_minutes_5_seconds_before(self):
        self.log_in()
        start, end = self.get_valid_datetime(17)
        self.post_valid_reservation(start, end, 'A')

    @freeze_time("2015-11-11 17:00:00")
    def test_user_cannot_post_reservation_0_min_0_sec_before(self):
        self.log_in()
        res_d = {}
        start = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        end = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH = "XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted at the same time of now()"))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted at the same time of now()"))

    @freeze_time("2015-11-11 17:01:00")
    def test_user_cannot_post_reservation_kala_min_before(self):
        self.log_in()
        res_d = {}
        start = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        end = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        res_d['start'] = start
        res_d['end'] = end
        res_d['field'] = 'A'
        response = self.client.post(self.reservation_url, res_d, HTTP_X_REQUESTED_WITH = "XMLHttpRequest")
        self.assertEqual(response.status_code, 400, _("Reservation posted 1 minute after "))
        self.assertTrue(len(Reservation.objects.all())==0, _("Reservation posted at the same time of now()"))

    def post_valid_reservation(self, start, end, field):
        reservation_data = {}
        reservation_data['start'] = start
        reservation_data['end'] = end
        reservation_data['field'] = field
        self.client.post(self.reservation_url, reservation_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        t_start, t_end = self.reformat_startend_timestring(start, end)
        field_id = Field.objects.all().filter(name = field)
        done_reservations = Reservation.objects.all().filter(start = t_start, field = field_id, end = t_end)

        self.assertTrue(done_reservations.count() == 1, _('No reservation made with valid data'))

    def reformat_startend_timestring(self, start, end):
        def reformat_timestring(s):
            s = s.split("T")
            t = s[1].split(":")
            t[0] = str(int(t[0])-2)
            s[1] = ":".join(t)
            return " ".join(s) + "+00:00"
        return reformat_timestring(start), reformat_timestring(end)

    def get_valid_datetime(self, hour, dayz = 0):
        d = datetime.now() + timedelta(days = dayz)
        start = datetime(year=d.year, month=d.month, day=d.day, hour=hour, minute=0, second=0)
        end = datetime(year=d.year, month=d.month, day=d.day, hour=hour+1, minute=0, second=0)
        return start.strftime("%Y-%m-%dT%H:%M:%S"), end.strftime("%Y-%m-%dT%H:%M:%S")

    def test_anon_user_cannot_removeall_reservations(self):
        response = self.client.post(self.remove_all_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/remove/all/'))

    def test_anon_user_cannot_remove_specific_reservation(self):
        response = self.client.post(self.remove_url,  {'id':str(1)}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/remove/'))

    def test_anon_user_cannot_make_payment_for_reservation(self):
        response = self.client.post(self.payment_url, {'id':str(1)}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/reservation/payment/'))

