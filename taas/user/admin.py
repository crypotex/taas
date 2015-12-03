from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from . import models as user_models
from .forms import UserCreationForm, UserChangeFormAdmin


class UserAdmin(auth_admin.UserAdmin):
    add_form_template = 'admin/add_form.html'
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'budget')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Pins'), {'fields': ('pin', 'button_id')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('pin', 'last_login', 'date_joined')
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')

    form = UserChangeFormAdmin
    add_form = UserCreationForm

# Unregister default models
admin.site.unregister(Group)

# Register models
admin.site.register(user_models.User, UserAdmin)
