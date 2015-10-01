import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms

logger = logging.getLogger(__name__)


def register_user(request):
    if request.method == 'POST':
        user_form = forms.UserCreationForm(request.POST, prefix='user_creation_form')
        if user_form.is_valid():
            user_form.save()
            logger.info('Unverified user with email %s has been successfully registered.'
                        % user_form.cleaned_data.get('email'))

            return HttpResponseRedirect('success')
    else:
        user_form = forms.UserCreationForm(prefix='user_creation_form')

    return render(request, 'user_registration.html', {'user_creation_form': user_form})
