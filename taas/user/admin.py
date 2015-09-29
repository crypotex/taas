from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


class UserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'last_login'
    )
    list_filter = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']

# Unregister default models
admin.site.unregister(Group)

# Register models
admin.site.register(models.User, UserAdmin)
