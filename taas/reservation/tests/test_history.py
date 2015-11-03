from datetime import datetime, timedelta
from http import client as http_client

from django.test import TransactionTestCase

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
            'month': datetime.today().month,
            'year': datetime.today().year
        }
        self._ensure_table_has_not_been_created(data)

    def test_user_does_not_get_other_user_reservations(self):
        ReservationFactory.create_batch(3, paid=True)
        data = {
            'month': datetime.today().month,
            'year': datetime.today().year
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

    def test_user_cannot_delete_past_paid_reservations(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = ReservationFactory(start=datetime.now() + timedelta(minutes=15),
                                         end=datetime.now() + timedelta(hours=1, minutes=15),
                                         user=self.user, paid=True)
        response = self.client.post(ReservationFactory.get_remove_url(), {'id': reservation.id},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, http_client.BAD_REQUEST)
        self.assertEqual(response.content.decode('utf-8'), "Cannot delete paid reservation.")
        self.assertTrue(Reservation.objects.filter(id=reservation.id).exists())
        self.assertNotEqual(User.objects.get(id=self.user.id).budget, reservation.price)

    def _ensure_table_has_not_been_created(self, data):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.history_url, data)
        self.assertEqual(response.status_code, http_client.OK)

        self.assertNotIn('<thead>', response.content.decode("utf-8"))
        self.assertNotIn('<tbody>', response.content.decode("utf-8"))
