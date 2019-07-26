# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Subscription, Application, Installation


# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    model = Application

    list_display = (
            'name',
            'uuid',
            'version',
            )

    ordering = (
        'name',)


@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    model = Installation

    list_display = (
        'id',
        'timestamp',
        'version',
        'type',
        'data',
    )

    ordering = (
        'timestamp',)


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
