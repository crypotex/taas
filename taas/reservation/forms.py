from django.forms import ModelForm
from .models import Reservation

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ['date_created']