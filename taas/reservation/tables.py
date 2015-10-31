import django_tables2 as tables
from django.utils.safestring import mark_safe

from taas.reservation.models import Reservation


class HistoryTable(tables.Table):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'field')

    image = tables.Column(attrs={"th": {"hidden": "True"}}, orderable=False, empty_values=())

    def render_image(self, record):
        from taas.reservation.views import can_delete_paid_reservation

        if can_delete_paid_reservation(record.start.astimezone(tz=None)):
            return mark_safe('<img id="%s" src="/static/img/clear.png" onClick="remove_reservation(this.id)" />'
                             % record.id)

        return ''
