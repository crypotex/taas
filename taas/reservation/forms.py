import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from taas.reservation.models import Field


class ReservationForm(forms.Form):
    field = forms.CharField(max_length=1)
    start = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S'])
    end = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%S'])

    def clean(self):
        super(ReservationForm, self).clean()
        if self.errors:
            return

        start = self.cleaned_data.get('start').replace(tzinfo=None)
        current = datetime.datetime.now()
        if start <= current:
            raise forms.ValidationError(_("Date should not be in the past."))
        elif (start-current) < datetime.timedelta(minutes=15):
            raise forms.ValidationError(_("There should be atleast 15 minutes before reservation"))
        else:
            end = self.cleaned_data.get('end').replace(tzinfo=None)
            if end < start:
                raise forms.ValidationError(_("Start date should be earlier than end date."))

        field = Field.objects.filter(name=self.cleaned_data['field'])
        if not field.exists():
            forms.ValidationError(_("Field does not exist."))
