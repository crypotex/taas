from http import client as http_client

from django.test import TestCase

from taas.user.tests.factories import UserFactory


class UserBalanceTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.balance_url = UserFactory.get_update_balance_url()

    def test_anonymous_user_cannot_add_money_to_the_balance(self):
        response = self.client.get(self.balance_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/user/balance/'))

    def test_logged_in_user_can_add_money_to_the_balance(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)
        response = self.client.get(self.balance_url)
        self.assertEqual(response.status_code, http_client.OK)
