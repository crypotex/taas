import json
import logging

from datetime import timedelta, date
from decimal import Decimal
from hashlib import sha512

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, DetailView, FormView
from django_tables2 import RequestConfig

from taas.reservation.forms import ReservationForm, HistoryForm, PasswordForm
from taas.reservation.models import Field, Reservation, Payment
from taas.reservation.tables import HistoryTable
from taas.user.mixins import LoggedInMixin
from taas.user.models import User

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


@login_required()
def remove_unpaid_reservations(request):
    if request.is_ajax():
        Reservation.objects.filter(user=request.user, paid=False).delete()
        return http.HttpResponse("Success")

    return http.HttpResponseForbidden(_("Error"))


def get_payment_order(amount, reference):
    data = {
        'shop': settings.MAKSEKESKUS['shop_id'],
        'amount': amount,
        'reference': reference
    }

    return json.dumps(data, cls=DjangoJSONEncoder)


def get_payment_mac(order):
    encoded_order = (order + settings.MAKSEKESKUS['secret_key']).encode('utf-8')
    hashed_order = sha512(encoded_order).hexdigest()
    return hashed_order.upper()


class ReservationList(LoggedInMixin, ListView):
    template_name = 'reservation_list.html'
    ordering = 'start'
    context_object_name = 'reservation_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        reservations = self.get_queryset()
        if not reservations.exists():
            return http.HttpResponseForbidden()

        return super(ReservationList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        total_price = self.queryset.aggregate(total_price=Sum('field__cost'))['total_price']

        old_staged = Payment.objects.filter(type=Payment.STAGED, user=self.request.user)
        if old_staged.exists():
            old_staged.delete()

        payment = Payment.objects.create(type=Payment.STAGED, amount=total_price,
                                         user=self.request.user)
        for reservation in self.queryset:
            payment.reservation_set.add(reservation)

        order_json = get_payment_order(total_price, payment.id)

        kwargs['total_price'] = total_price
        kwargs['json'] = order_json
        kwargs['mac'] = get_payment_mac(order_json)
        kwargs['host'] = settings.MAKSEKESKUS['host']
        return super(ReservationList, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.queryset = Reservation.objects.filter(user=self.request.user, paid=False)

        return super(ReservationList, self).get_queryset()


@csrf_exempt
@login_required
def payment_cancelled(request):
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(permitted_methods=['POST'])

    confirm_json = request.POST.get('json')
    confirm_mac1 = request.POST.get('mac')
    if not confirm_json or not confirm_mac1:
        return http.HttpResponseBadRequest()

    confirm_mac2 = get_payment_mac(confirm_json)
    if confirm_mac1 != confirm_mac2:
        return http.HttpResponseBadRequest()

    reference = json.loads(confirm_json)['reference']
    if reference.startswith('B'):
        messages.add_message(request, messages.INFO, _('Adding money to budget was cancelled.'))
        return http.HttpResponseRedirect(reverse_lazy('homepage'))

    staged_payments = Payment.objects.filter(id=reference)
    if staged_payments.exists():
        staged_payments.delete()

    messages.add_message(request, messages.INFO, _('Payment was cancelled.'))
    return http.HttpResponseRedirect(reverse_lazy('homepage'))


@csrf_exempt
@login_required
def payment_success(request):
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(permitted_methods=['POST'])

    confirm_json = request.POST.get('json')
    confirm_mac1 = request.POST.get('mac')
    if not confirm_json or not confirm_mac1:
        return http.HttpResponseBadRequest()

    confirm_mac2 = get_payment_mac(confirm_json)
    if confirm_mac1 != confirm_mac2:
        return http.HttpResponseBadRequest()

    payment = json.loads(confirm_json)
    reference = payment['reference']
    amount = payment['amount']
    if reference.startswith('B'):
        user_id = reference[1:]
        user = User.objects.get(id=user_id)
        user.budget += Decimal(amount)
        user.save()
        Payment.objects.create(type=Payment.TRANSACTION, user=user, amount=payment['amount'])

        messages.add_message(request, messages.SUCCESS, _('Successfully added money to the budget.'))
        return http.HttpResponseRedirect(reverse_lazy('homepage'))

    try:
        staged_payment = Payment.objects.get(id=reference)
        staged_payment.type = Payment.TRANSACTION
        staged_payment.reservation_set.update(paid=True)
        staged_payment.save()
    except (Payment.DoesNotExist, Payment.MultipleObjectsReturned):
        return http.HttpResponseServerError(_('Error occurred. Please contact administrator.'))

    messages.add_message(request, messages.SUCCESS, _('Successfully paid for the reservations.'))

    return http.HttpResponseRedirect(reverse_lazy('homepage'))


class BudgetPaymentView(LoggedInMixin, FormView):
    form_class = PasswordForm
    template_name = 'budget_payment.html'
    http_method_names = ['post', 'get']

    def get(self, request, *args, **kwargs):
        staged_payments = Payment.objects.filter(type=Payment.STAGED, user=self.request.user)
        if not staged_payments.exists() or staged_payments.count() > 1:
            return http.HttpResponseForbidden()

        self.payment = staged_payments.first()
        return super(BudgetPaymentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        staged_payments = Payment.objects.filter(type=Payment.STAGED, user=self.request.user)
        if not staged_payments.exists() or staged_payments.count() > 1:
            return http.HttpResponseForbidden()

        self.payment = staged_payments.first()
        return super(BudgetPaymentView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(BudgetPaymentView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        total_price = self.payment.amount
        if total_price > self.request.user.budget:
            messages.add_message(self.request, messages.INFO, _('You do not have enough money.'))
            return http.HttpResponseRedirect(reverse('reservation_list'))

        self.request.user.budget -= total_price
        self.request.user.save()

        self.payment.reservation_set.update(paid=True)
        self.payment.type = Payment.BUDGET
        self.payment.save()

        messages.add_message(self.request, messages.SUCCESS, _('Successfully paid for the reservations.'))
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
