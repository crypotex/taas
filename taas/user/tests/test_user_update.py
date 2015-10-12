from http import client as http_client

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from taas.user.models import User
from taas.user.tests.factories import UserFactory


class UserUpdateTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.update_url = UserFactory.get_update_url()

    def test_anonymous_user_is_redirected_to_the_login_page(self):
        response = self.client.get(self.update_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/user/update/'))

    def test_logged_in_user_can_access_update_page(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_logged_in_user_can_update_his_first_name(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        data = {
            'first_name': 'Test',
            'last_name': self.user.last_name,
            'phone_number': self.user.phone_number,
        }
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, expected_url=self.update_url)

        user = User.objects.get(email=self.user.email)
        self.assertEqual(user.first_name, 'Test')

    def test_logged_in_user_can_update_his_last_name(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        data = {
            'first_name': self.user.first_name,
            'last_name': 'Test',
            'phone_number': self.user.phone_number,
        }
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, expected_url=self.update_url)

        user = User.objects.get(email=self.user.email)
        self.assertEqual(user.last_name, 'Test')

    def test_logged_in_user_can_update_his_phone_number(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone_number': '536358',
        }
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, expected_url=self.update_url)

        user = User.objects.get(email=self.user.email)
        self.assertEqual(user.phone_number, '536358')

    def test_logged_in_user_can_update_his_password_with_valid_parameters(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        data = self._get_post_data()
        passwords = {
            'change_password': 'on',
            'old_password': 'isherenow',
            'new_password1': 'test',
            'new_password2': 'test',
        }
        data.update(passwords)
        response = self.client.post(self.update_url, data)
        self.assertRedirects(response, expected_url=self.update_url)

        response = self.client.login(username=self.user.email, password='test', follow=True)
        self.assertTrue(response)

    def test_logged_in_user_cannot_update_his_password_with_invalid_old_password(self):
        data = self._get_post_data()
        passwords = {
            'change_password': 'on',
            'old_password': 'blabla',
            'new_password1': 'test',
            'new_password2': 'test',
        }
        data.update(passwords)
        self._ensure_logged_in_user_cannot_update_his_password_with_invalid_parameters(data)

    def test_logged_in_user_cannot_update_his_password_with_not_matching_new_passwords(self):
        data = self._get_post_data()
        passwords = {
            'change_password': 'on',
            'old_password': 'isherenow',
            'new_password1': 'test',
            'new_password2': 'test2',
        }
        data.update(passwords)
        self._ensure_logged_in_user_cannot_update_his_password_with_invalid_parameters(data)

    def test_logged_in_user_cannot_update_his_password_without_first_new_password(self):
        data = self._get_post_data()
        passwords = {
            'change_password': 'on',
            'old_password': 'isherenow',
            'new_password1': '',
            'new_password2': 'test2',
        }
        data.update(passwords)
        self._ensure_logged_in_user_cannot_update_his_password_with_invalid_parameters(data)

    def test_logged_in_user_cannot_update_his_password_without_second_new_password(self):
        data = self._get_post_data()
        passwords = {
            'change_password': 'on',
            'old_password': 'isherenow',
            'new_password1': 'test',
            'new_password2': '',
        }
        data.update(passwords)
        self._ensure_logged_in_user_cannot_update_his_password_with_invalid_parameters(data)

    # Helper methods
    def _ensure_logged_in_user_cannot_update_his_password_with_invalid_parameters(self, data):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, http_client.OK)

        can_login = self.client.login(username=self.user.email, password=data['new_password1'], follow=True)
        self.assertFalse(can_login)

    def _get_post_data(self):
        return {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone_number': self.user.phone_number,
        }


class UserDeactivationTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        mail.outbox = []
        self.deactivate_url = UserFactory.get_deactivate_url()
        self.homepage_url = reverse('homepage')

    def test_anonymous_user_is_redirected_to_the_login_page(self):
        response = self.client.get(self.deactivate_url)
        self.assertRedirects(response, expected_url=UserFactory.get_login_url(next='/user/deactivate/'))

    def test_logged_in_user_can_access_deactivation_page(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)
        response = self.client.get(self.deactivate_url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_logged_in_user_can_deactivate_his_account(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)

        response = self.client.post(self.deactivate_url, {'password': 'isherenow'})
        self.assertRedirects(response, expected_url=self.homepage_url)

        user = User.objects.get(email=self.user.email)
        self.assertFalse(user.is_active)

    def test_user_receives_email_notification_after_deactivation(self):
        self.client.login(username=self.user.email, password='isherenow', follow=True)
        self.client.post(self.deactivate_url, {'password': 'isherenow'})

        self.assertIn(self.user.email, [email.to[0] for email in mail.outbox])

    def test_admin_receives_email_notification_after_deactivation(self):
        with self.settings(ADMIN_EMAILS=['test.email@example.com']):
            self.client.login(username=self.user.email, password='isherenow', follow=True)
            self.client.post(self.deactivate_url, {'password': 'isherenow'})
            self.assertIn('test.email@example.com', [email.to[0] for email in mail.outbox])
