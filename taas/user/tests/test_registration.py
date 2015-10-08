from http import client as http_client

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase

from taas.user.tests.factories import UserFactory
from taas.user.models import User


class UserRegistrationTest(TransactionTestCase):
    def setUp(self):
        self.registration_url = UserFactory.get_registration_url()
        self.form_data = UserFactory.get_form_data()

    def test_anonymous_user_can_access_registration_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot access registration page.')

    def test_user_can_register_with_valid_arguments(self):
        response = self.client.post(self.registration_url, self.form_data, follow=True)
        self.assertRedirects(response, expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertIn('User has been successfully registered.',
                      [m.message for m in response.context['messages']])

    def test_user_recieves_email_after_successful_registration(self):
        response = self.client.post(self.registration_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, http_client.OK)
        self.assertIn(self.form_data['email'], [email.to[0] for email in mail.outbox])

    def test_admin_recieves_email_after_user_successful_registration(self):
        with self.settings(ADMIN_EMAILS=['test.email@example.com']):
            response = self.client.post(self.registration_url, self.form_data, follow=True)
            self.assertEqual(response.status_code, http_client.OK)
            self.assertIn('test.email@example.com', [email.to[0] for email in mail.outbox])

    def test_user_registration_creates_user(self):
        self.client.post(self.registration_url, self.form_data, follow=True)
        user = User.objects.filter(email=self.form_data['email'])
        self.assertTrue(user.exists(), 'User is not created in database.')
        self.assertEqual(user.count(), 1, 'Multiple users with same email.')

    def test_registered_user_is_inactive(self):
        self.client.post(self.registration_url, self.form_data, follow=True)
        user = User.objects.get(email=self.form_data['email'])
        self.assertFalse(user.is_active, 'User is activated after registration.')

    def test_user_cannot_register_with_invalid_confirm_password(self):
        self._ensure_user_cannot_register_with_invalid_field_value('password2', 'invalid')

    def test_user_cannot_register_without_email(self):
        self._ensure_user_cannot_register_with_invalid_field_value('email', '')

    def test_user_cannot_register_without_first_name(self):
        self._ensure_user_cannot_register_with_invalid_field_value('first_name', '')

    def test_user_cannot_register_without_last_name(self):
        self._ensure_user_cannot_register_with_invalid_field_value('last_name', '')

    def test_user_cannot_register_without_first_password(self):
        self._ensure_user_cannot_register_with_invalid_field_value('password1', '')

    # Helper methods
    def _ensure_user_cannot_register_with_invalid_field_value(self, field_name, field_value):
        self.form_data[field_name] = field_value

        response = self.client.post(self.registration_url, self.form_data)
        self.assertEqual(response.status_code, http_client.OK)

        user = User.objects.filter(email=self.form_data['email'])
        self.assertFalse(user.exists(), 'User can register without %s.' % field_name)
