import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from django.http import Http404

from django.http import HttpResponseRedirect
from . import models
from . import forms

logger = logging.getLogger(__name__)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class ReservationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    success_message = _('Reservation has been successfully made.')
    success_url = reverse_lazy('homepage')
    template_name = 'reservation.html'
    model = models.Reservation
    form_class = forms.ReservationForm

    #Authentication
    login_url = reverse_lazy("user_login_form")
    redirect_authenticated_users = True

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not request.user.is_authenticated():
            return HttpResponseRedirect
        tuser = request.user
        ## For post method security
        if not tuser.is_authenticated:
            raise Http404

        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
        raise Http404
        ##return render(request, self.template_name, {'form': form})

    '''
    Pole vaja hetkel
    def form_valid(self, form):
        logger.info('Reservation made by %s for %s has been successfully registered.'
                    % form.cleaned_data.get('user'), form.cleaned_data.get('start_date'))
        return super(ReservationView, self).form_valid(form)
    '''