from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'TrailNet Profile',
            {'fields': ('role', 'contact_number', 'profile_photo', 'bike_setup')},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            'TrailNet Profile',
            {'fields': ('email', 'role')},
        ),
    )
