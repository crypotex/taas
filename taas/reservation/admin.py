from django.contrib import admin

from taas.reservation.models import Reservation, Field, Payment


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', 'id', 'payment')
    list_display = ('id', 'start', 'end', 'user', 'field', 'payment')
    list_filter = ('paid',)
    search_fields = ('id', 'user__email', 'field__name', 'payment__id')
    ordering = ('id', 'start', 'end', 'field')


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')
    search_fields = ('name', 'cost')
    ordering = ('name', 'cost')


class ReservationInLine(admin.StackedInline):
    model = Reservation
    fields = ('start', 'end', 'field')
    readonly_fields = ('start', 'end', 'field')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PaymentAdmin(admin.ModelAdmin):
    inlines = (ReservationInLine,)
    list_display = ('id', 'type', 'amount', 'date_created', 'user')
    search_fields = ('id', 'type', 'amount', 'user__email')
    ordering = ('id', 'type', 'amount', 'user__email')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_reservations(self, obj):
        return obj.reservation_set


# Register models
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(Payment, PaymentAdmin)
