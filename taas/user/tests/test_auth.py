from http import client as http_client

from django.test import TransactionTestCase
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from .factories import UserFactory
from taas.user.forms import UserForm


class UserLoginTest(TransactionTestCase):
    user1 = {'Username':'user', 'Password': "admin"}
    inv_user1 = {'username':"userssss", 'password': "admin"}
    inv_user2 = {'username':"user", 'password': "ues"}

    login_url = 'http://testserver' + reverse('user_login_form')

    def test_user_can_access_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot log in.')

    def test_user_can_login_with_valid_arguments(self):
        response = self.client.post(self.login_url, self.user1)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot login.')

    ### Have to change these two tests
    def test_user_cannot_login_with_invalid_username(self):
        response = self.client.post(self.login_url, self.inv_user1)
        ##self.assertEqual(response.errors['__all__'][0], _('Passwords are not equal.'))

    def test_user_cannot_login_with_invalid_password(self):
        response = self.client.post(self.login_url, self.inv_user2)
        ##self.assertNotEqual(response.status_code, http_client.OK, 'User can login with invalid password.')
