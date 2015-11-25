import django_tables2 as tables
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from taas.reservation.models import Reservation


class HistoryTable(tables.Table):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'field')
        attrs = {"id": "bookings"}

    update = tables.Column(attrs={"th": {"hidden": "True"}}, orderable=False, empty_values=())
    delete = tables.Column(attrs={"th": {"hidden": "True"}}, orderable=False, empty_values=())

    def render_delete(self, record):
        if record.can_delete():
            return mark_safe(
                '<img id="%s" src="/static/img/clear.png" alt="delete" onClick="remove_reservation(this.id)" />'
                % record.id)
        return ''

    def render_update(self, record):
        if record.can_update():
            reverse('detail_reservation', kwargs={'pk': record.id})
            return mark_safe(
                '<img id="%s" alt="update" src="/static/img/change.png" onClick="update_reservation(this.id)" />'
                % record.id)
        return ''

class HistoryListTable(tables.Table):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'field')
        attrs = {"id": "bookings"}

    delete = tables.Column(attrs={"th": {"hidden": "True"}}, orderable=False, empty_values=())

    def render_delete(self, record):
        if record.can_delete():
            return mark_safe(
                '<img id="%s" src="/static/img/clear.png" alt="delete" onClick="remove_reservation(this.id)" />'
                % record.id)
        return ''