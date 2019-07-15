# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product, BarCode


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'description',
                    'uuid',
                    'parentUuid',
                    'type',
                    'group',
                    )

    search_fields = ('name', 'description',
                     )
    ordering = ('name', 'type',
                )
    list_filter = ('group', 'type', 'allowToSell',
                   )


@admin.register(BarCode)
class BarCodeAdmin(admin.ModelAdmin):
    list_display = ('code',
                    )

