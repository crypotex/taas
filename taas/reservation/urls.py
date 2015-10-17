from django.conf.urls import url

from taas.reservation import views


urlpatterns = [
    url(r'^fields/$', views.get_fields, name='fields'),
    url(r'^all/$', views.get_reservations, name='all_reservations'),
    url(r'^add/$', views.add_reservation, name='add_reservation'),
    url(r'^remove/$', views.remove_reservation, name='remove_reservation'),
    url(r'^remove/all/$', views.remove_unpaid_reservations, name='remove_reservation'),
    url(r'^list/$', views.ReservationList.as_view(), name='reservation_list'),
    url(r'^payment/$', views.reservation_payment, name='reservation_payment'),
]
