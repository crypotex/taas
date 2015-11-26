from http import client
from django.test import TransactionTestCase

from taas.reservation import models
from taas.reservation import models as user_models
from taas.reservation.tests import factories
from taas.user.tests.factories import UserFactory
from django.core.urlresolvers import reverse


class ReservationListTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.list_url = factories.ReservationFactory.get_reservation_list_url()

    def test_anonymous_user_cannot_access_reservation_list_page(self):
        response = self.client.get(self.list_url)
        self.assertRedirects(response, UserFactory.get_login_url(next='/reservation/list/'))

    def test_user_cannot_access_reservation_list_page_without_staged_reservations(self):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.list_url)
        self.assertRedirects(response,
                             expected_url=reverse('homepage'),
                             status_code=client.FOUND,
                             target_status_code=client.OK)

    def test_user_can_access_reservation_list_page_with_staged_reservations(self):
        self.client.login(username=self.user.email, password='isherenow')
        factories.ReservationFactory.create_batch(3, user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

    def test_reservation_list_page_creates_valid_staged_payment(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservations = factories.ReservationFactory.create_batch(3, user=self.user)
        amount = sum(reservation.field.cost for reservation in reservations)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        staged_payment = models.Payment.objects.get(user=self.user, type=models.Payment.STAGED)
        self.assertEqual(staged_payment.amount, amount)
        self.assertEqual(list(staged_payment.reservation_set.all()), reservations)

    def test_previously_staged_payment_is_removed_after_accessing_reservation_list_page(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservations = factories.ReservationFactory.create_batch(3, user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        reservations += factories.ReservationFactory.create_batch(3, user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        staged_payment = models.Payment.objects.get(user=self.user, type=models.Payment.STAGED)
        amount = sum(reservation.field.cost for reservation in reservations)
        self.assertEqual(staged_payment.amount, amount)
        self.assertEqual(list(staged_payment.reservation_set.all()), reservations)

    def test_staged_payment_is_removed_after_removing_connected_reservations(self):
        self.client.login(username=self.user.email, password='isherenow')
        factories.ReservationFactory.create_batch(3, user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        reservations = models.Reservation.objects.filter(user=self.user)
        for reservation in reservations:
            reservation.delete()

        staged_payment = models.Payment.objects.filter(user=self.user, type=models.Payment.STAGED)
        self.assertFalse(staged_payment.exists())


class BudgetPaymentTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.budget_url = factories.PaymentFactory.get_budget_payment_url()
        self.list_url = factories.ReservationFactory.get_reservation_list_url()

    def test_anonymous_user_cannot_access_budget_payment_page(self):
        response = self.client.get(self.budget_url)
        self.assertRedirects(response, UserFactory.get_login_url(next='/reservation/payment/budget/'))

    def test_user_cannot_access_budget_page_without_staged_payment(self):
        self.client.login(username=self.user.email, password='isherenow')
        response = self.client.get(self.budget_url)
        self.assertEqual(response.status_code, client.FORBIDDEN)

    def test_user_can_access_budget_page_with_staged_payment(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = factories.ReservationFactory(user=self.user)
        payment = factories.PaymentFactory(user=self.user, type=models.Payment.STAGED)
        payment.reservation_set.add(reservation)

        response = self.client.get(self.budget_url)
        self.assertEqual(response.status_code, client.OK)

    def test_user_cannot_pay_with_budget_with_invalid_password(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservation = factories.ReservationFactory(user=self.user)
        payment = factories.PaymentFactory(user=self.user, type=models.Payment.STAGED)
        payment.reservation_set.add(reservation)

        response = self.client.post(self.budget_url, {'password': 'blablabla'})
        self.assertEqual(response.status_code, client.OK)

        staged_payment = models.Payment.objects.filter(user=self.user, type=models.Payment.BUDGET)
        self.assertFalse(staged_payment.exists())

    def test_user_cannot_pay_with_budget_with_not_enough_money(self):
        self.client.login(username=self.user.email, password='isherenow')
        factories.ReservationFactory.create_batch(3, user=self.user)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        response = self.client.post(self.budget_url, {'password': 'isherenow'})
        self.assertRedirects(response, '/reservation/list/')

    def test_user_can_pay_with_budget_with_enough_money(self):
        self.client.login(username=self.user.email, password='isherenow')
        reservations = factories.ReservationFactory.create_batch(3, user=self.user)
        amount = sum(reservation.price for reservation in reservations)
        self.user.budget = amount
        self.user.save()

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, client.OK)

        response = self.client.post(self.budget_url, {'password': 'isherenow'})
        self.assertRedirects(response, '/')
        self.assertEqual(user_models.User.objects.get(id=self.user.id).budget, 0)

        staged_payment = models.Payment.objects.filter(user=self.user, type=models.Payment.BUDGET)
        self.assertTrue(staged_payment.exists())

