from datetime import timedelta
from http import client as http_client

from django.test import TransactionTestCase
from django.utils import timezone

from taas.reservation.models import Reservation
from taas.reservation.tests.factories import ReservationFactory
from taas.user.models import User
from taas.user.tests.factories import UserFactory


class HistoryListTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.history_url = ReservationFactory.get_reservation_history_url()

    def test_anonymous_user_cannot_access_history_page(self):
        response = self.client.get(self.history_url)
        self.assertRedirects(response, UserFactory.get_login_url(next='/reservation/history/'))

    def test_authenticated_user_can_access_history_page(self):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_user_does_not_get_unpaid_reservations(self):
        ReservationFactory.create_batch(3, user=self.user)
        data = {
            'month': timezone.datetime.today().month,
            'year': timezone.datetime.today().year
        }
        self._ensure_table_has_not_been_created(data)

    def test_user_does_not_get_other_user_reservations(self):
        ReservationFactory.create_batch(3, paid=True)
        data = {
            'month': timezone.datetime.today().month,
            'year': timezone.datetime.today().year
        }
        self._ensure_table_has_not_been_created(data)

    def test_user_can_delete_future_paid_reservations(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = ReservationFactory(paid=True, user=self.user)
        response = self.client.post(ReservationFactory.get_remove_url(), {'id': reservation.id},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(response.status_code, http_client.OK)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
        self.assertEqual(User.objects.get(id=self.user.id).budget, reservation.price)

    def test_user_cannot_delete_paid_reservations_in_past(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = ReservationFactory(start=timezone.now() - timedelta(minutes=15),
                                         end=timezone.now() - timedelta(hours=1, minutes=15),
                                         user=self.user, paid=True)
        response = self.client.post(ReservationFactory.get_remove_url(), {'id': reservation.id},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), "Cannot delete the reservation.")
        self.assertTrue(Reservation.objects.filter(id=reservation.id).exists())
        self.assertNotEqual(User.objects.get(id=self.user.id).budget, reservation.price)

    def _ensure_table_has_not_been_created(self, data):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.history_url, data)
        self.assertEqual(response.status_code, http_client.OK)

        self.assertNotIn('<thead>', response.content.decode("utf-8"))
        self.assertNotIn('<tbody>', response.content.decode("utf-8"))


class ReservationUpdateTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.reservation = ReservationFactory(user=self.user)
        self.detail_url = ReservationFactory.get_reservation_detail_url(self.reservation.id)

    def test_anonymous_user_cannot_access_reservation_update_page(self):
        response = self.client.get(self.detail_url)
        self.assertRedirects(response, UserFactory.get_login_url(
            next='/reservation/update/%s/' % self.reservation.id))

    def test_user_can_update_future_paid_reservation(self):
        self.reservation.paid = True
        self.reservation.save()
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_user_cannot_update_future_unpaid_reservation(self):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, http_client.NOT_FOUND)

    def test_user_cannot_update_other_user_reservation(self):
        self.client.login(username=self.user.email, password='isherenow')
        other_reservation = ReservationFactory(paid=True)
        response = self.client.get(ReservationFactory.get_reservation_detail_url(other_reservation.id))
        self.assertEqual(response.status_code, http_client.NOT_FOUND)

    def test_user_cannot_update_reservation_in_past(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = ReservationFactory(start=timezone.now() - timedelta(minutes=15),
                                         end=timezone.now() - timedelta(hours=1, minutes=15),
                                         user=self.user, paid=True)
        response = self.client.get(ReservationFactory.get_reservation_detail_url(reservation.id))
        self.assertEqual(response.status_code, http_client.NOT_FOUND)

    def test_user_cannot_update_reservation_with_invalid_field_id(self):
        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d %H'),
            'end': end.strftime('%Y-%m-%d %H'),
            'field': 5
        }
        self._ensure_user_cannot_update_reservation(data)

    def test_user_cannot_update_reservation_with_invalid_field_name(self):
        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d %H'),
            'end': end.strftime('%Y-%m-%d %H'),
            'field': 'asad'
        }
        self._ensure_user_cannot_update_reservation(data)

    def test_user_cannot_update_reservation_with_invalid_start_date(self):
        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d %H'),
            'field': self.reservation.field.id
        }
        self._ensure_user_cannot_update_reservation(data)

    def test_user_cannot_update_reservation_with_invalid_end_date(self):
        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d %H'),
            'end': end.strftime('%Y-%m-%d'),
            'field': self.reservation.field.id
        }
        self._ensure_user_cannot_update_reservation(data)

    def test_user_can_update_reservation_with_valid_data(self):
        self.reservation.paid = True
        self.reservation.save()
        self.client.login(username=self.user.email, password='isherenow')

        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d %H'),
            'end': end.strftime('%Y-%m-%d %H'),
            'field': self.reservation.field.id
        }

        response = self.client.post(self.detail_url + 'confirm/', data)
        self.assertRedirects(response, ReservationFactory.get_reservation_history_url())

    def test_anonymous_user_cannot_access_confirmation_page(self):
        self.reservation.paid = True
        self.reservation.save()

        start = self.reservation.start + timedelta(hours=1)
        end = self.reservation.end + timedelta(hours=1)
        data = {
            'start': start.strftime('%Y-%m-%d %H'),
            'end': end.strftime('%Y-%m-%d %H'),
            'field': self.reservation.field.id
        }

        response = self.client.post(self.detail_url + 'confirm/', data)
        self.assertRedirects(response, UserFactory.get_login_url(
            next='/reservation/update/%s/confirm/' % self.reservation.id))

    def test_user_cannot_make_get_request_to_confirmation_page(self):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.detail_url + 'confirm/')
        self.assertEqual(response.status_code, http_client.METHOD_NOT_ALLOWED)

    # Helper methods
    def _ensure_user_cannot_update_reservation(self, data):
        self.reservation.paid = True
        self.reservation.save()
        self.client.login(username=self.user.email, password='isherenow')

        response = self.client.post(self.detail_url + 'confirm/', data)
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)
