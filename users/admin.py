# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username',
        'email',
        'userId',
        'first_name',
        'last_name',
        'last_login')

    list_filter = (
        'date_joined',
        'last_login',
    )
    readonly_fields = (
        'date_joined',
        'date_updated',
        'last_login',
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'userId',
            )
        }),

        (u'Персональная информация', {
            'fields': (
                'first_name',
                'last_name',
            )
        }),

        (u'Важные даты', {
            'fields': (
                'last_login',
                'date_joined',
                'date_updated',
            )
        }),

        (u'Права доступа', {
            'fields': (
                'is_admin',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes':
                ('wide',),
            'fields': (
                'email',
                'password',
                'is_admin',
            )
        }),
    )

    search_fields = (
        'email',)

    ordering = (
        'date_joined',)

    filter_horizontal = (
        'groups',
        'user_permissions',
    )