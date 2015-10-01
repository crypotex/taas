from http import client as http_client

from django.test import TransactionTestCase
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm


from .factories import UserFactory


class UserLoginTest(TransactionTestCase):
    def setUp(self):
        self.user = UserFactory(is_active=True)
        self.login_url = UserFactory.get_login_url()

    def test_user_can_access_login(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot log in.')

    def test_user_can_login_with_valid_arguments(self):
        data = {'username': self.user.email, 'password': self.user.password}
        login_form = AuthenticationForm(data)
        # self.assertEqual(response.status_code, http_client.OK, 'User cannot login.')
        self.assertTrue(login_form.is_valid())

    ### Have to change these two tests
    def test_user_cannot_login_with_invalid_username(self):
        self.user.email = "vale@email.com"
        login_form = AuthenticationForm(data=UserFactory.get_form_data())
        self.assertFalse(login_form.is_valid())
        self.assertEqual(login_form.errors['__all__'][0],
                         _('Please enter a correct username and password. Note that both fields may be case-sensitive.'))

    def test_user_cannot_login_with_invalid_password(self):
        response = self.client.post(self.login_url, self.inv_user2)
        ##self.assertNotEqual(response.status_code, http_client.OK, 'User can login with invalid password.')

    #Helper methods
    def get_user_dict(self, user):
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'password1': 'isherenow',
            'password2': 'isherenow'
        }
