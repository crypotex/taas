import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from . import models
from . import forms

logger = logging.getLogger(__name__)


class ReservationView(SuccessMessageMixin, CreateView):
    success_message = _('Reservation has been successfully made.')
    success_url = reverse_lazy('homepage')
    template_name = 'reservation.html'
    model = models.Reservation
    form_class = forms.ReservationForm

    def form_valid(self, form):
        logger.info('Reservation made by %s for %s has been successfully registered.'
                    % form.cleaned_data.get('user'), form.cleaned_data.get('start_date'))
        ##return super(UserRegisterView, self).form_valid(form)
        return True