import logging

from decimal import Decimal
from datetime import timedelta, date, datetime

from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render_to_response, render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, FormView
from django_tables2 import RequestConfig

from taas.reservation.forms import ReservationForm, HistoryForm
from taas.reservation.models import Field, Reservation
from taas.reservation.tables import HistoryTable
from taas.user.mixins import LoggedInMixin

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs = super(HomePageView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            reservations = Reservation.objects.filter(
                user=self.request.user,
                paid=False).order_by('date_created')

            if reservations.exists():
                kwargs['is_unpaid'] = True
                first_unpaid = reservations.first().date_created.astimezone(tz=None)
                kwargs['expire_date'] = (first_unpaid + timedelta(minutes=10)). \
                    strftime("%Y/%m/%d %H:%M:%S")

        return kwargs


def get_fields(request):
    if request.is_ajax():
        fields = Field.objects.all().values('id', 'name')

        return http.JsonResponse(list(fields), safe=False)

    return http.HttpResponseForbidden()


def get_reservations(request):
    if request.is_ajax():
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')

        if start and end:
            reservations = Reservation.objects.filter(
                start__gte=start,
                end__lte=end,
            )
            entries = []
            for reservation in reservations:
                if not reservation.paid:
                    if not request.user.is_authenticated():
                        continue
                    if reservation.user != request.user:
                        color = '#FF8C00'
                    else:
                        color = '#008000'
                elif reservation.user == request.user:
                    color = '#483D8B'
                else:
                    color = '#7B68EE'

                start_time = reservation.start.astimezone(tz=None)
                end_time = reservation.end.astimezone(tz=None)
                entry = {
                    'id': reservation.id,
                    'start': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'resources': reservation.field.id,
                    'editable': False,
                    'color': color
                }
                if request.user.is_staff:
                    entry['title'] = reservation.id

                entries.append(entry)

            return http.JsonResponse(entries, safe=False)

    return http.HttpResponseForbidden()


@login_required()
def add_reservation(request):
    if request.is_ajax() and request.method == 'POST':
        form = ReservationForm(data=request.POST)
        if form.is_valid():
            data = {
                'field': Field.objects.get(name=form.cleaned_data['field']),
                'start': form.cleaned_data['start'],
                'end': form.cleaned_data['end'],
                'user': request.user
            }
            reservation = Reservation.objects.filter(
                field=data['field'],
                start__lt=data['end'],
                end__gt=data['start']
            )
            if not reservation.exists():
                Reservation.objects.create(**data)

            return http.HttpResponse("Success")

    return http.HttpResponseBadRequest("Error")


def check_unpaid_reservations(user):
    reservations = Reservation.objects.filter(user=user, paid=False)
    return reservations.exists()


def can_delete_paid_reservation(reservation_start):
    diff = (reservation_start.replace(tzinfo=None) - datetime.now())

    return divmod(diff.days * 86400 + diff.seconds, 60)[0] >= 15


@login_required()
def remove_reservation(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            reservation_id = int(request.POST.get('id'))
        except ValueError:
            return http.HttpResponseBadRequest("Invalid key.")

        reservations = Reservation.objects.filter(id=reservation_id)
        if reservations.exists():
            reservation = reservations.first()

            if not reservation.paid:
                reservation.delete()
            elif can_delete_paid_reservation(reservation.start.astimezone(tz=None)):
                request.user.budget += reservation.price
                request.user.save()
                reservation.delete()
            else:
                return http.HttpResponseBadRequest("Cannot delete paid reservation.")

        response = check_unpaid_reservations(request.user)
        return http.JsonResponse({'response': response}, safe=False)

    return http.HttpResponseBadRequest("Not allowed.")


class ReservationList(LoggedInMixin, ListView):
    template_name = 'payment.html'
    ordering = 'start'
    context_object_name = 'reservation_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        reservations = self.get_queryset()
        if not reservations.exists():
            return http.HttpResponseForbidden()

        return super(ReservationList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        total_price = sum(reservation.price for reservation in self.queryset)
        kwargs['total_price'] = total_price

        return super(ReservationList, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = Reservation.objects.filter(user=self.request.user, paid=False)

        return super(ReservationList, self).get_queryset()


@login_required()
def remove_unpaid_reservations(request):
    if request.is_ajax():
        Reservation.objects.filter(user=request.user, paid=False).delete()
        return http.HttpResponse("Success")

    return http.HttpResponseForbidden("Error")


@login_required()
def reservation_payment(request):
    # Temporary view
    reservations = Reservation.objects.filter(user=request.user, paid=False)
    reservations.update(paid=True)
    messages.add_message(request, messages.SUCCESS, _('Successfully paid for the reservations.'))

    return http.HttpResponseRedirect(reverse('homepage'))


@login_required()
def history(request):
    template = 'history.html'
    if request.method == 'POST':
        form = HistoryForm(data=request.POST)
        if form.is_valid():
            current_month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
        else:
            return http.HttpResponseBadRequest()
    else:
        form = HistoryForm()
        current_month = date.today().month
        year = date.today().year

    data = {'form': form}
    next_month = 1 if current_month == 12 else current_month + 1
    reservations = Reservation.objects.filter(
        user=request.user,
        paid=True,
        start__gt=date(year, current_month, 1),
        end__lt=date(year, next_month, 1)
    ).order_by('start')
    if reservations.exists():
        table = HistoryTable(reservations)
        RequestConfig(request, paginate={"per_page": 20}).configure(table)
        data['table'] = table

    return render(request, template, data)
