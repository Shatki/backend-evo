# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
from users.models import User
from .constants import SUBSCRIPTION_TYPES, SUBSCRIPTION_TYPE_DEFAULT


# Create your models here.
class Subscription(models.Model):
    class Meta:
        verbose_name = u'подписка на приложение'
        verbose_name_plural = u'подписки на приложение'
        db_table = u'subscriptions'

    # Идентификатор подписки. "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
    subscriptionId = models.UUIDField(verbose_name=u'идентификатор подписки', primary_key=True,
                                      default=uuid.uuid4, null=False)

    # Идентификатор приложения. "productId": "c0d01x35-5193-4cc2-9bfb-be20e0679498",
    productId = models.UUIDField(verbose_name=u'идентификатор приложения', default=uuid.uuid4,
                                 unique=True, null=False)

    # Идентификатор пользователя в Облаке Эвотор. "userId": "01-000000000000001",
    #userId = models.CharField(verbose_name=u'идентификатор пользователя в Облаке Эвотор', max_length=18,
    #                          default="01-000000000000001", editable=True, unique=True, null=False)
    userId = models.ForeignKey(User, verbose_name=u'идентификатор пользователя в Облаке Эвотор',
                               null=False, on_delete=models.CASCADE, default=1)

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
    type = models.CharField(verbose_name=u'тип события', max_length=40, choices=SUBSCRIPTION_TYPES,
                            default=SUBSCRIPTION_TYPE_DEFAULT)

    # "planId": "example",
    # Идентификатор тарифа, который вы создаёте на портале разработчиков.
    planId = models.CharField(verbose_name=u'идентификатор тарифа', max_length=30, default="", null=True)

    # "trialPeriodDuration": "P14DT",
    # Строка вида PnDT, где n – количество дней бесплатного периода, доступных пользователю в момент активации тарифа.
    trialPeriodDuration = models.CharField(verbose_name=u'количество дней бесплатного периода', max_length=5,
                                           default='P07DT')
    # Количество оплаченных устройств. "deviceNumber": 35
    deviceNumber = models.IntegerField(u'количество оплаченных устройств', default=1)

    def __str__(self):
        return str(self.subscriptionId)
