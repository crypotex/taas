import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.http.request import QueryDict
from django.shortcuts import render

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
        p_user = request.user

        ## For post method security
        if not p_user.is_authenticated:
            return HttpResponseRedirect(self.login_url)

        post_data = QueryDict('', mutable=True)
        post_data.update(request.POST)
        post_data.update({'user':str(p_user.id)})

        form = self.form_class(post_data)
        if form.is_valid():
            reservation = form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, 'reservation.html', {'form':form,})