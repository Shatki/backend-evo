# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    model = Token
    list_display = (
        'key',
        'user',
        'created',
        'updated',
    )

    readonly_fields = (
        'key',
        'created',
        'updated'
    )

