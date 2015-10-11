from django.conf.urls import url

from .views import get_fields

urlpatterns = [
    # url(r'^make/$', ReservationView.as_view(), name='reservation_form'),
    url(r'^get_fields/$', get_fields, name='get_ajax_fields'),
]