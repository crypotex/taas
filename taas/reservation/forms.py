from django.forms import ModelForm
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from taas.reservation.models import Reservation, Field


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        exclude = ['date_created']

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()

        if cleaned_data['date'] < datetime.now().date():
            raise ValidationError(_("Date should start from now."))
        if cleaned_data['date'] == datetime.now().date():
            temp_timeslot = datetime.strptime(str(cleaned_data['timeslot']) + ":00", "%H:%M").time()
            cur_time = datetime.now().time()
            hourdiff = temp_timeslot.hour - cur_time.hour
            mindiff = cur_time.minute - temp_timeslot.minute
            if hourdiff <= 0:
                raise ValidationError(_("You cannot do reservation into the past"))
            if hourdiff == 1 and mindiff <30:
                raise ValidationError(_("Your reservation is supposed to start atleast 30 minutes from now"))

        temp_reservations = Reservation.objects.filter(date = cleaned_data['date'],
                                                      timeslot = cleaned_data['timeslot'])
        taken_fields = []
        if temp_reservations.count()>0:
            for reservation in temp_reservations:
                for field in reservation.fields.all():
                    taken_fields.append(field)
        for field in taken_fields:
            for c_field in cleaned_data['fields']:
                if field == c_field:
                    raise ValidationError(_("That field on that timeslot is already taken"))
