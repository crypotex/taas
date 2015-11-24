from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(auth_forms.UserCreationForm):
    required_css_class = 'required'

    password1 = forms.CharField(label=_("Password"), min_length=8, max_length=64,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), min_length=8, max_length=64,
                                widget=forms.PasswordInput)

    class Meta(object):
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number'
        )


class UserChangeFormAdmin(auth_forms.UserChangeForm):
    class Meta(object):
        model = get_user_model()
        fields = '__all__'


class UserUpdateForm(forms.ModelForm):
    change_password = forms.BooleanField(label=_("Change password"), required=False)
    new_password1 = forms.CharField(label=_("New password"), min_length=8, max_length=64, required=False,
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), min_length=8, max_length=64, required=False,
                                    widget=forms.PasswordInput)
    old_password = forms.CharField(label=_("Old password"), required=False,
                                   widget=forms.PasswordInput)

    class Meta(object):
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone_number',
                  'old_password', 'new_password1', 'new_password2']

    def clean(self):
        super(UserUpdateForm, self).clean()

        if self.errors:
            return

        is_password_change = self.cleaned_data.get('change_password', False)
        if is_password_change:
            old_pass = self.cleaned_data['old_password']
            new_pass1 = self.cleaned_data['new_password1']
            new_pass2 = self.cleaned_data['new_password2']

            if not old_pass:
                raise forms.ValidationError(_('Old password is required.'))
            elif not new_pass1:
                raise forms.ValidationError(_('New password is required.'))
            elif not new_pass2:
                raise forms.ValidationError(_('New password confirmation is required.'))

            if not self.instance.check_password(old_pass):
                raise forms.ValidationError(
                    _('Your old password was entered incorrectly. Please enter it again.'))
            if new_pass1 != new_pass2:
                raise forms.ValidationError(_("The two new password fields didn't match."))

    def save(self, commit=True):
        if self.cleaned_data['change_password']:
            self.instance.set_password(self.cleaned_data['new_password1'])
            if commit:
                self.instance.save()

        return super(UserUpdateForm, self).save(commit)


class UserDeactivateForm(forms.Form):
    def __init__(self, user, **kwargs):
        super(UserDeactivateForm, self).__init__(**kwargs)
        self.user = user

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError(
                _('Your password was entered incorrectly. Please enter it again.'))


class customPasswordSetForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), min_length=8, max_length=64,
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), min_length=8, max_length=64,
                                    widget=forms.PasswordInput)
