import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms

logger = logging.getLogger(__name__)


def register_user(request):
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, prefix='user_form')
        if user_form.is_valid():
            user_form.save()
            logger.info('Unverified user with username %s has been successfully registered.'
                        % request.POST.get('user_form-username'))

            return HttpResponseRedirect('success')
    else:
        user_form = forms.UserForm(prefix='user_form')

    return render(request, 'user_registration.html', {'user_form': user_form})
