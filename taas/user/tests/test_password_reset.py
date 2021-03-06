from http import client as http_client
import re

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from taas.user.tests.factories import UserFactory


class UserPasswordResetTest(TestCase):
    def setUp(self):
        self.disabled_user = UserFactory()
        self.active_user = UserFactory(is_active=True)
        self.reset_url = UserFactory.get_password_reset_url()
        mail.outbox = []

    def test_logged_in_user_cannot_reset_his_password(self):
        self.client.login(username=self.active_user.email, password='isherenow')
        response = self.client.get(self.reset_url)
        self.assertRedirects(response, expected_url=reverse('homepage'))

    def test_logged_out_user_can_reset_his_password(self):
        response = self.client.get(self.reset_url)
        self.assertEqual(response.status_code, http_client.OK)

    def test_active_user_can_reset_his_password(self):
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        self.assertIn(self.active_user.email, [email.to[0] for email in mail.outbox])
        self.assertIn('Password reset', [email.subject for email in mail.outbox])

    def test_disabled_user_cannot_reset_his_password(self):
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
        new_pw = "testtest"
        # Request password reset
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        # Get generated link from the email
        link = re.findall(r'(http://\S+)', mail.outbox[0].body)[0]

        # Access generated link and submit new password
        data = {'new_password1': new_pw, 'new_password2': new_pw}
        response = self.client.post(link, data, follow=True)
        self.assertRedirects(response, expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertEqual('Your password has been set. You may go ahead and log in now.',
                         list(response.context['messages'])[0].message)

        # Check if user can login with the new password
        login_data = {'username': self.active_user.email, 'password': new_pw}
        response = self.client.post(UserFactory.get_login_url(), login_data)
        self.assertRedirects(response, expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)

    def test_active_user_cannot_change_his_too_short_password_with_generated_link(self):
        new_pw = "kala"
        # Request password reset
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        # Get generated link from the email
        link = re.findall(r'(http://\S+)', mail.outbox[0].body)[0]

        # Access generated link and submit new password
        data = {'new_password1': new_pw, 'new_password2': new_pw}
        response = self.client.post(link, data, follow=True)
        self.assertEqual("Password reset unsuccessful", response.context_data['title'])

    def test_active_user_cannot_change_password_to_empty_string(self):
        new_pw = ""
        # Request password reset
        self.client.post(self.reset_url, data={'email': self.active_user.email}, follow=True)

        # Get generated link from the email
        link = re.findall(r'(http://\S+)', mail.outbox[0].body)[0]

        # Access generated link and submit new password
        data = {'new_password1': new_pw, 'new_password2': new_pw}
        response = self.client.post(link, data, follow=True)
        self.assertEqual("Password reset unsuccessful", response.context_data['title'])