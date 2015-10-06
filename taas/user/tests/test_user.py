from http import client as http_client

from django.test import TransactionTestCase
from django.utils.translation import ugettext_lazy as _

from .factories import UserFactory
from taas.user.forms import UserCreationForm


class UserRegistrationTest(TransactionTestCase):
    def setUp(self):
        self.registration_url = UserFactory.get_registration_url()
        self.form_data = UserFactory.get_form_data()

    def test_anonymous_user_can_access_registration_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, http_client.OK, 'User cannot access registration page.')

    def test_user_can_register_with_valid_arguments(self):
        form = UserCreationForm(self.form_data)
        self.assertTrue(form.is_valid(), 'User cannot register.')

    def test_user_cannot_register_with_invalid_confirm_password(self):
        self.form_data['password2'] = 'invalid'
        form = UserCreationForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register with invalid confirm password.')
        self.assertEqual(form.errors['password2'][0], _("The two password fields didn't match."))

    def test_user_cannot_register_without_email(self):
        self.form_data['email'] = ''
        form = UserCreationForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without email.')
        self.assertEqual(form.errors['email'][0], _('This field is required.'))

    def test_user_cannot_register_without_first_name(self):
        self.form_data['first_name'] = ''
        form = UserCreationForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without first name.')
        self.assertEqual(form.errors['first_name'][0], _('This field is required.'))

    def test_user_cannot_register_without_last_name(self):
        self.form_data['last_name'] = ''
        form = UserCreationForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without last name.')
        self.assertEqual(form.errors['last_name'][0], _('This field is required.'))

    def test_user_cannot_register_without_password(self):
        self.form_data['password1'] = ''
        form = UserCreationForm(self.form_data)

        self.assertFalse(form.is_valid(), 'User can register without password.')
        self.assertEqual(form.errors['password1'][0], _('This field is required.'))
