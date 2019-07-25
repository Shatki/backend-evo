# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Subscription


# Register your models here.
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription

    list_display = (
        'subscriptionId',
        'productId',
        'userId',
        'timestamp',
        'type',
        )

    list_filter = (
        'timestamp',
        'type',
    )

    fieldsets = (
        (u'Подписка', {
            'fields': (
                'subscriptionId',
                'productId',
                'userId',
                'trialPeriodDuration',
                'deviceNumber',
            )
        }),

        (u'Информация о продлении', {
            'fields': (
                'timestamp',
                'sequenceNumber',
                'type',
                'planId',
            )
        }),
    )

    search_fields = (
        'userId',)

    ordering = (
        'timestamp',)
