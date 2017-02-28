from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST

from taas.reservation import views


urlpatterns = [
    url(r'^fields/$', views.get_fields, name='fields'),
    url(r'^all/$', views.get_reservations, name='all_reservations'),
    url(r'^add/$', views.add_reservation, name='add_reservation'),
    url(r'^update/(?P<pk>\d+)/$', views.ReservationDetailView.as_view(), name='detail_reservation'),
    url(r'^update/(?P<pk>\d+)/confirm/$', require_POST(views.UpdateReservationView.as_view()),
        name='update_reservation'),
    url(r'^remove/$', views.remove_reservation, name='remove_reservation'),
    url(r'^remove/all/$', views.remove_unpaid_reservations, name='remove_all_reservations'),
    url(r'^list/$', views.ReservationList.as_view(), name='reservation_list'),
    url(r'^payment/success/$', views.payment_success, name='payment_success'),
    url(r'^payment/cancel/$', views.payment_cancelled, name='payment_cancel'),
    url(r'^payment/transaction/$', views.ProceedTransactionView.as_view(), name='proceed_transaction'),
    url(r'^payment/budget/$', views.BudgetPaymentView.as_view(), name='budget_payment'),
    url(r'^expire/$', views.get_expire_time, name='get_expire_time'),
    url(r'^history/$', views.history, name='reservation_history'),
    url(r'^help/', TemplateView.as_view(template_name="help.html")),
    url(r'^privacy_policy/', TemplateView.as_view(template_name="privacy_policy.html"))
]
