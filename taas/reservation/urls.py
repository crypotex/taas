from django.conf.urls import url

from taas.reservation.views import get_events, get_fields, initialize_events, ReservationList


urlpatterns = [
    url(r'^get_fields/$', get_fields, name='get_ajax_fields'),
    url(r'^get_events/$', get_events, name='get_ajax_events'),
    url(r'^initialize/$', initialize_events, name='init_ajax_events'),
    url(r'^payment/$', ReservationList.as_view(), name='reservation_list'),
]