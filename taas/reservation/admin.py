from django.contrib import admin

from taas.reservation.models import Reservation, Field


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'id')

    list_display = ('id', 'start', 'end', 'user', 'field')
    list_filter = ('paid',)
    search_fields = ('id',)
    ordering = ('id', 'start', 'end', 'field')


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')
    search_fields = ('name', 'cost')
    ordering = ('name', 'cost')

# Register models
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Field, FieldAdmin)
