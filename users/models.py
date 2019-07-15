# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

SUBSCRIPTION_CREATED = u'SubscriptionCreated'
ADDONS_UPDATED = u'AddonsUpdated'
SUBSCRIPTION_ACTIVATED = u'SubscriptionActivated'
SUBSCRIPTION_RENEWED = u'SubscriptionRenewed'
SUBSCRIPTION_TERMS_CHANGED = u'SubscriptionTermsChanged'
SUBSCRIPTION_TERMINATION_REQUESTED = u'SubscriptionTerminationRequested'
SUBSCRIPTION_TERMINATED = u'SubscriptionTerminated'

SUBSCRIPTION_TYPE_DEFAULT = SUBSCRIPTION_CREATED

SUBSCRIPTION_TYPES = {
    (SUBSCRIPTION_CREATED, u'новая подписка'),
    (ADDONS_UPDATED, u'список платных опций, выбранных пользователем'),
    (SUBSCRIPTION_ACTIVATED, u'подписка активирована'),
    (SUBSCRIPTION_RENEWED, u'подписка продлена на следующий период'),
    (SUBSCRIPTION_TERMS_CHANGED, u'изменились условия подписки'),
    (SUBSCRIPTION_TERMINATION_REQUESTED, u'запрос на завершение подписки'),
    (SUBSCRIPTION_TERMINATED, u'подписка завершена')
}


class User(AbstractUser):
    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'
        db_table = 'users'

    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email


class Subscription(models.Model):
    class Meta:
        verbose_name = u'подписка на приложение'
        verbose_name_plural = u'подписки на приложение'

    # Идентификатор подписки. "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
    subscriptionId = models.UUIDField(verbose_name=u'идентификатор подписки', primary_key=True, default=uuid.uuid4,
                                      editable=False, unique=True, null=False)

    # Идентификатор приложения. "productId": "c0d01x35-5193-4cc2-9bfb-be20e0679498",
    productId = models.UUIDField(verbose_name=u'идентификатор приложения', default=uuid.uuid4,
                                 editable=False, unique=True, null=False)

    # Идентификатор пользователя в Облаке Эвотор. "userId": "01-000000000000001",
    userId = models.UUIDField(verbose_name=u'идентификатор пользователя в Облаке Эвотор', default=uuid.uuid4,
                              editable=False, unique=True, null=False)

    # Дата и время отправки события. В соответствовии с ISO 8601. "timestamp": "2017-04-20T18:26:37.753+0000",
    timestamp = models.DateTimeField(verbose_name=u'дата и время отправки события')

    # "sequenceNumber": 4,
    # Номер события в последовательности. Номер непрерывно возрастает начиная с единицы.
    # Необходим для соблюдения порядка обработки событий.
    # Номер события уникален в рамках подписки (subscriptionId),
    # таким образом, при переустановке приложения номерация событий начнётся сначала
    sequenceNumber = models.IntegerField(verbose_name=u'номер события в последовательности', null=False)

    # "type": "SubscriptionCreated",
    # Типы событий:
    #
    # SubscriptionCreated – новая подписка. Сообщает о том, что пользователь установил приложение в Личном кабинете.
    #       Приходит в начале пробного периода или перед сообщением об успешной оплате, если пробного периода нет.
    # AddonsUpdated – список платных опций, выбранных пользователем.
    # SubscriptionActivated – подписка активирована. Сообщает об успешной оплате.
    # SubscriptionRenewed – подписка продлена на следующий период. Сообщает об успешной оплате очередного периода.
    # SubscriptionTermsChanged – изменились условия подписки, например, тарифный план или количество устройств.
    # SubscriptionTerminationRequested – Пользователь отправил запрос на завершение подписки (удалил приложение
    #        из Личного кабинета). Пользователь может возобновить подписку до окончания оплаченного периода.
    # SubscriptionTerminated – Подписка завершена. Приходит если не прошла регулярная оплата,
    #       независимо от того запросил пользователь завершение подписки или нет.
    type = models.CharField(verbose_name=u'тип события', max_length=40)



    # "planId": "example",
    # "trialPeriodDuration": "P14DT",
    # "deviceNumber": 35
