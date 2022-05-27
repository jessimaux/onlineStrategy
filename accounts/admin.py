from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group

from .models import Account


class AccountAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'phone_number',
                    'staff', 'superuser')
    list_filter = ('staff', 'superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name', 'date_of_birth', 'phone_number',
                                      'region', 'city', 'municipality', 'status', 'education_organization',
                                      'education_class')}),
        ('Permissions', {'fields': ('staff', 'superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)