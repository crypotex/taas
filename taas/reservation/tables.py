import django_tables2 as tables
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from taas.reservation.models import Reservation


class HistoryTable(tables.Table):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'field')
        attrs = {"id": "bookings"}

    update = tables.Column(orderable=False, empty_values=())
    delete = tables.Column(orderable=False, empty_values=())

    def render_delete(self, record):
        if record.can_delete():
            return mark_safe(
                '<img class="%s" src="/static/img/clear.png" alt="delete" '
                'onClick="remove_reservation(this.className)" />'
                % record.id)
        return ''

    def render_update(self, record):
        if record.can_update():
            reverse('detail_reservation', kwargs={'pk': record.id})
            return mark_safe(
                '<img class="%s" alt="update" src="/static/img/change.png" '
                'onClick="update_reservation(this.className)" />'
                % record.id)
        return ''


class ReservationListTable(tables.Table):
    class Meta:
        model = Reservation
        fields = ('start', 'end', 'field')
        attrs = {"id": "bookings"}

    price = tables.Column(verbose_name=_('price (€)'), accessor='field.cost')
    delete = tables.Column(orderable=False, empty_values=())

    def render_delete(self, record):
        if record.can_delete():
            return mark_safe(
                '<img id="%s" src="/static/img/clear.png" alt="delete" onClick="remove_reservation(this.id)" />'
                % record.id)
        return ''
