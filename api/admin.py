# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import Token, Log


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


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    model = Log
    list_display = (
        'datetime',
        'status',
        'headers',
        'request',
        'response',
    )

    readonly_fields = (
        'datetime',
    )

