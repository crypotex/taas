from http import client as http_client
import re

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from taas.user.models import User
from taas.user.tests.factories import UserFactory


class UserPasswordResetTest(TestCase):
    def setUp(self):
        self.disabled_user = UserFactory()
        self.active_user = UserFactory(is_active=True)
        self.reset_url = UserFactory.get_password_reset_url()
        mail.outbox = []

    def test_active_user_can_reset_his_password(self):
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        self.assertIn(self.active_user.email, [email.to[0] for email in mail.outbox])
        self.assertIn('Password reset', [email.subject for email in mail.outbox])

    def test_disabled_user_can_reset_his_password(self):
        self.client.post(self.reset_url, data={'email': self.disabled_user.email}, follow=True)

        self.assertNotIn(self.disabled_user.email, [email.to[0] for email in mail.outbox])
        self.assertNotIn('Password reset', [email.subject for email in mail.outbox])

    def test_invalid_email_is_not_sent(self):
        data = {'email': 'lol@example.com'}
        self.client.post(self.reset_url, data, follow=True)

        self.assertNotIn(self.disabled_user.email, [email.to[0] for email in mail.outbox])
        self.assertNotIn('Password reset', [email.subject for email in mail.outbox])

    def test_active_user_with_valid_email_can_access_generated_link(self):
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)
        link = re.findall(r'(https?://\S+)', mail.outbox[0].body)[0]

        response = self.client.get(link)
        self.assertEqual(response.status_code, http_client.OK)

    def test_active_user_can_change_his_password_with_generated_link(self):
        # Request password reset
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        # Get generated link from the email
        link = re.findall(r'(http://\S+)', mail.outbox[0].body)[0]

        # Access generated link and submit new password
        data = {'new_password1': 'test', 'new_password2': 'test'}
        response = self.client.post(link, data, follow=True)
        self.assertRedirects(response, expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertEqual('Your password has been set. You may go ahead and log in now.',
                         list(response.context['messages'])[0].message)

        # Check if user can login with the new password
        login_data = {'username': self.active_user.email, 'password': 'test'}
        response = self.client.post(UserFactory.get_login_url(), login_data)
        self.assertRedirects(response, expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
