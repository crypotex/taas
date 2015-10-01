from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import QueryDict

import factory
import factory.fuzzy


class UserFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = get_user_model()

    username = factory.Sequence(lambda n: 'taavi%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    first_name = factory.Sequence(lambda n: 'Taavi%s' % n)
    last_name = factory.Sequence(lambda n: 'Tonu%s' % n)
    phone_number = factory.Sequence(lambda n: '555831%s' % n)
    password = factory.PostGenerationMethodCall('set_password', 'isherenow')
    is_staff = False
    is_active = False
    is_superuser = False

    @classmethod
    def get_registration_url(cls):
        return 'http://testserver' + reverse('user_registration_form')

    @classmethod
    def get_form_data(cls):
        return {
            'username': 'taavi',
            'email': 'taavi@example.com',
            'first_name': 'Taavi',
            'last_name': 'Tonu',
            'phone_number': '555123456',
            'password1': 'test',
            'password2': 'test'
        }
