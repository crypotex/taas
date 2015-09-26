from http import client as http_client

from django.test import TransactionTestCase
from django.utils.translation import ugettext_lazy as _

from .factories import UserFactory
from taas.user.forms import UserForm


class UserPermissionTest(TransactionTestCase):
    def setUp(self):
        self.registration_url = UserFactory.get_registration_url()
        self.form_data = UserFactory.get_form_data()

    def test_anonymous_user_can_access_registration_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot access registration page.')

    def test_user_can_register_with_valid_arguments(self):
        form = UserForm(self.form_data)
        self.assertTrue(form.is_valid(), 'User cannot register.')

    def test_user_cannot_register_with_invalid_confirm_password(self):
        self.form_data['password_confirm'] = 'invalid'
        form = UserForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register with invalid confirm password.')
        self.assertEqual(form.errors['__all__'][0], _('Passwords are not equal.'))

    def test_user_cannot_register_without_username(self):
        self.form_data['username'] = ''
        form = UserForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without username.')
        self.assertEqual(form.errors['username'][0], _('This field is required.'))

    def test_user_cannot_register_without_email(self):
        self.form_data['email'] = ''
        form = UserForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without username.')
        self.assertEqual(form.errors['email'][0], _('This field is required.'))

    def test_user_cannot_register_without_password(self):
        self.form_data['password'] = ''
        form = UserForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without username.')
        self.assertEqual(form.errors['password'][0], _('This field is required.'))
