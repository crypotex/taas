from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from taas.reservation.models import Field


class ReservationForm(forms.Form):
    field = forms.CharField(max_length=10)
    start = forms.DateTimeField()
    end = forms.DateTimeField()

    def clean(self):
        super(ReservationForm, self).clean()
        if self.errors:
            return

        start = self.cleaned_data.get('start')
        current = timezone.localtime(timezone.now())
        if start <= current:
            raise forms.ValidationError(_("Date should not be in the past."))
        elif (start-current) < timezone.timedelta(minutes=15):
            raise forms.ValidationError(_("There should be at least 15 minutes before reservation"))
        elif start.hour not in range(8, 23):
            raise forms.ValidationError(_("Invalid reservation time."))
        else:
            end = self.cleaned_data.get('end')
            if end < start:
                raise forms.ValidationError(_("Start date should be earlier than end date."))

        field = Field.objects.filter(name=self.cleaned_data['field'])
        if not field.exists():
            forms.ValidationError(_("Field does not exist."))


MONTHS = [
    (1, _('January')),
    (2, _('February')),
    (3, _('March')),
    (4, _('April')),
    (5, _('May')),
    (6, _('June')),
    (7, _('July')),
    (8, _('August')),
    (9, _('September')),
    (10, _('October')),
    (11, _('November')),
    (12, _('December')),
]

YEARS = [(year, year)
         for year in range(timezone.datetime.today().year - 1, timezone.datetime.today().year + 2)]


class HistoryForm(forms.Form):
    month = forms.ChoiceField(choices=MONTHS, initial=timezone.datetime.today().month)
    year = forms.ChoiceField(choices=YEARS, initial=timezone.datetime.today().year)
