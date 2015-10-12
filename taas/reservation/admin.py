from django.contrib import admin

from taas.reservation.models import Reservation, Field


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)

# Register models
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Field)
