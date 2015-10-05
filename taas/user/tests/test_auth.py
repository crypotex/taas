from http import client as http_client

from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import UserFactory


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.login_data = {'username': self.user.email, 'password': 'isherenow'}
        self.login_url = UserFactory.get_login_url()
        self.logout_url = UserFactory.get_logout_url()

    def test_user_can_access_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, http_client.OK,
                         'User cannot log in with valid data.')

    def test_user_can_login_with_valid_arguments(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertRedirects(response,
                             expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk,
                         'User cannot login with valid data.')

    def test_user_cannot_login_with_invalid_username(self):
        self.login_data['username'] = 'vale@email.com'
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, http_client.OK,
                         'User can login with invalid email.')

    def test_user_cannot_login_with_invalid_password(self):
        self.login_data['password'] = 'invalid'
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, http_client.OK,
                         'User can login with invalid password.')

    def test_user_can_login_and_logout(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertRedirects(response,
                             expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk,
                         'User cannot login with valid data.')
        response = self.client.post(self.logout_url,  self.login_data)
        self.assertRedirects(response,
                             expected_url=reverse('homepage'),
                             status_code=http_client.FOUND,
                             target_status_code=http_client.OK)

        self.assertNotIn('_auth_user_id', self.client.session, "User cannot logout with valid data.")