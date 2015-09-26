from django import forms
from django.utils.translation import ugettext_lazy as _

from taas.user.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=128, label=_('Password'), widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=128, label=_('Confirm password'), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_confirm',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError(_('Passwords are not equal.'))

        return self.cleaned_data
