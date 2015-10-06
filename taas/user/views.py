import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from . import forms
from . import models

logger = logging.getLogger(__name__)


class UserRegisterView(SuccessMessageMixin, CreateView):
    success_message = _('User has been successfully registered.')
    success_url = reverse_lazy('homepage')
    template_name = 'user_registration.html'
    model = models.User
    form_class = forms.UserCreationForm

    def form_valid(self, form):
        logger.info('Unverified user with email %s has been successfully registered.'
                    % form.cleaned_data.get('email'))
        return super(UserRegisterView, self).form_valid(form)
