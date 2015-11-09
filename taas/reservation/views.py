import json
import logging
from datetime import timedelta, date
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
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
                paid=False
            ).order_by('date_created')

            if reservations.exists():
                kwargs['is_unpaid'] = True
                first_unpaid = reservations.first().get_date_created()
                kwargs['expire_date'] = (first_unpaid + timedelta(minutes=10)).strftime("%Y/%m/%d %H:%M:%S")

        return kwargs


def get_fields(request):
    if request.is_ajax():
        fields = Field.objects.all().values('id', 'name')

        return http.JsonResponse(list(fields), safe=False)

    return http.HttpResponseForbidden()


def get_calendar_entities(start, end, user, update=None):
    colors = settings.COLORS
    entries = []
    reservations = Reservation.objects.filter(
        start__gte=start,
        end__lte=end,
    )

    for reservation in reservations:
        if not reservation.paid:
            if not user.is_authenticated() or update is not None:
                continue
            if reservation.user != user:
                color = colors['unpaid']['others']
            else:
                color = colors['unpaid']['owner']
        elif reservation.user == user:
            if reservation.id == update:
                color = colors['update']
            else:
                color = colors['paid']['owner']
        elif user.is_authenticated():
            color = colors['paid']['others']
        else:
            color = colors['paid']['anonymous']

        start_time = reservation.get_start()
        end_time = reservation.get_end()
        entry = {
            'id': reservation.id,
            'start': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'resources': reservation.field.id,
            'color': color,
            'overlap': False,
            'slotEventOverlap': False

        }
        if user.is_staff:
            entry['title'] = reservation.id

        if update == reservation.id:
            entry['startEditable'] = True

        entries.append(entry)

    return entries


def get_reservations(request):
    if request.is_ajax():
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')

        if start and end:
            # FixMe: SQL injection can be applied here.
            return http.JsonResponse(get_calendar_entities(start, end, request.user), safe=False)

    return http.HttpResponseBadRequest()


@login_required()
def add_reservation(request):
    def create(start, end, field, user):
        data = {
            'field': field,
            'start': start,
            'end': end,
            'user': request.user
        }

        reservation = Reservation.objects.filter(
            field=data['field'],
            start__lt=data['end'],
            end__gt=data['start']
        )
        if not reservation.exists():
            Reservation.objects.create(**data)

    if request.is_ajax() and request.method == 'POST':
        form = ReservationForm(data=request.POST)
        if form.is_valid():
            field = Field.objects.get(name=form.cleaned_data['field'])
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            hours_diff = (end - start).seconds / 3600

            for h in range(0, int(hours_diff)):
                start = form.cleaned_data['start'] + timedelta(hours=h)
                end = start + timedelta(hours=1)
                create(start, end, field, request.user)

            return http.HttpResponse(_("Success"))

    return http.HttpResponseBadRequest(_("Error"))


def check_unpaid_reservations(user):
    reservations = Reservation.objects.filter(user=user, paid=False)
    return reservations.exists()


@login_required()
def remove_reservation(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            reservation_id = int(request.POST.get('id'))
        except ValueError:
            return http.HttpResponseBadRequest(_("Invalid key."))

        reservations = Reservation.objects.filter(id=reservation_id, user=request.user)
        if reservations.exists():
            reservation = reservations.first()

            if reservation.can_delete():
                if reservation.paid:
                    request.user.budget += reservation.price
                    request.user.save()
                reservation.delete()
            else:
                return http.HttpResponseBadRequest(_("Cannot delete the reservation."))

        response = check_unpaid_reservations(request.user)
        return http.JsonResponse({'response': response}, safe=False)

    return http.HttpResponseBadRequest(_("Not allowed."))


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

    return http.HttpResponseForbidden(_("Error"))


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
    if request.method != 'GET':
        return http.HttpResponseBadRequest()

    if 'month' in request.GET and 'year' in request.GET:
        form = HistoryForm(data=request.GET)
        if form.is_valid():
            current_month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])
        else:
            return http.HttpResponseBadRequest()
    else:
        form = HistoryForm()
        current_month = timezone.now().month
        year = timezone.now().year

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


@login_required()
def get_expire_time(request):
    if request.is_ajax():
        reservation_list = Reservation.objects.filter(user=request.user, paid=False).order_by("date_created")
        if reservation_list.exists():
            expire_datetime = reservation_list.first().get_date_created() + timedelta(minutes=10)
            diff = expire_datetime - timezone.localtime(timezone.now())
            timer = str(diff).split('.')[0].split(':', 1)[1]
            return http.JsonResponse({'response': timer}, safe=False)

        return http.JsonResponse({'response': "null"}, safe=False)

    return http.HttpResponseForbidden("Error")


class ReservationDetailView(LoggedInMixin, DetailView):
    model = Reservation
    template_name = 'reservation_update.html'

    def get_object(self, queryset=None):
        reservation = super(ReservationDetailView, self).get_object(queryset)
        if reservation.user == self.request.user and reservation.can_update():
            return reservation

        raise http.Http404()

    def get_context_data(self, **kwargs):
        context = super(ReservationDetailView, self).get_context_data(**kwargs)
        start = self.object.start.date()
        end = self.object.end.date() + timedelta(days=1)
        entities = get_calendar_entities(start, end, self.request.user, update=self.object.id)
        data = {
            'entities': json.dumps(entities),
            'form': ReservationForm,
            'start': self.object.start.strftime('%Y-%m-%d %H'),
            'end': self.object.end.strftime('%Y-%m-%d %H'),
            'field': self.object.field.name,
            'table_date': self.object.start.strftime('%Y-%m-%d')
        }
        context.update(data)

        return context


class UpdateReservationView(LoggedInMixin, FormView):
    form_class = ReservationForm
    success_url = reverse_lazy('reservation_history')
    template_name = 'reservation_update.html'

    def post(self, *args, **kwargs):
        reservation_id = kwargs.get('pk')
        if reservation_id is None:
            raise http.Http404()

        reservation = Reservation.objects.filter(id=reservation_id)
        if not reservation.exists():
            raise http.Http404()

        reservation = reservation.first()
        if reservation.user == self.request.user and reservation.can_update():
            self.object = reservation
            return super(UpdateReservationView, self).post(*args, **kwargs)

        raise http.Http404()

    def form_valid(self, form):
        self.object.start = form.cleaned_data['start']
        self.object.end = form.cleaned_data['end']
        try:
            field = int(form.cleaned_data['field'])
            self.object.field = Field.objects.get(id=field)
        except ValueError:
            self.object.field = Field.objects.get(name=form.cleaned_data['field'])

        self.object.save()

        return super(UpdateReservationView, self).form_valid(form)

    def form_invalid(self, form):
        return http.HttpResponseBadRequest()
