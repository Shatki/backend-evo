# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Store


# Register your models here.
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'address',
                    'uuid',
                    'code',
                    )

    search_fields = ('name', 'address')
    ordering = ('name',)
    # list_filter = ('name', 'address')
