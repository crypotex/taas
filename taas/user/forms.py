from django.contrib.auth import forms as auth_forms, get_user_model


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(object):
        model = get_user_model()
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            'phone_number'
        )


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(object):
        model = get_user_model()
        fields = '__all__'
