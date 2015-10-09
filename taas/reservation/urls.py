from django.conf.urls import url

from .views import ReservationView

urlpatterns = [
    url(r'^make/$', ReservationView.as_view(), name='reservation_form'),
]