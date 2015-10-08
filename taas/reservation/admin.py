from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from taas.reservation.models import Reservation, Field

class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('payment_sum', 'date_created')

# Register models
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Field)