from django.contrib.auth import forms as auth_forms, get_user_model


class UserCreationForm(auth_forms.UserCreationForm):
    required_css_class = 'required'

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


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(object):
        model = get_user_model()
        fields = '__all__'
