import logging

from django import http
from datetime import timedelta, timezone
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from taas.reservation.models import Field, Reservation
from taas.reservation.forms import ReservationForm, PaymentForm
from taas.user.mixins import LoggedInMixin

logger = logging.getLogger(__name__)


def get_fields(request):
    if request.is_ajax():
        fields = Field.objects.all().values('pk', 'name')
        for field in fields:
            field['id'] = field.pop('pk')

        return http.JsonResponse(list(fields), safe=False)

    return http.HttpResponseForbidden()


def get_events(request):
    if request.is_ajax():
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')

        if start and end:
            reservations = Reservation.objects.filter(
                start__gte=start,
                start__lte=end,
            )
            entries = []
            for reservation in reservations:
                color = ''
                if not reservation.payed:
                    if not request.user.is_authenticated():
                        continue
                    elif reservation.user != request.user:
                        color = '#FFFF00'
                    else:
                        color = '#008000'
                date_time = reservation.start.replace(tzinfo=timezone.utc).astimezone(tz=None)
                entry = {
                    'title': reservation.pk,
                    'start': date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': (date_time + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
                    'resources': reservation.field.pk,
                    'editable': False
                }
                if color:
                    entry['color'] = color
                entries.append(entry)

            return http.JsonResponse(entries, safe=False)

    return http.HttpResponseForbidden()


@login_required()
def initialize_events(request):
    if request.is_ajax() and request.method == 'POST':
        form = ReservationForm(data=request.POST)
        if form.is_valid():
            data = {
                'field': Field.objects.get(name=form.cleaned_data['field']),
                'user': request.user,
                'start': form.cleaned_data['start']
            }
            Reservation.objects.create(**data)
            return http.HttpResponse("Success")

    return http.HttpResponseBadRequest("Error")


class ReservationList(SuccessMessageMixin, LoggedInMixin, FormView):
    template_name = 'payment.html'
    success_message = _('You have successfully payed for your reservations.')
    success_url = reverse_lazy('homepage')
    form_class = PaymentForm
    def get_context_data(self, **kwargs):
        kwargs = super(ReservationList, self).get_context_data(**kwargs)
        kwargs['reservation_list'] = Reservation.objects.filter(user=self.request.user, payed=False)

        return kwargs

    def form_valid(self, form):
        queryset = Reservation.objects.filter(user=self.request.user, payed=False)
        for reservation in queryset:
            reservation.payed = True
            reservation.save()

        return super(ReservationList, self).form_valid(form)
