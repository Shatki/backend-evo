# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django_unixdatetimefield import UnixDateTimeField

import uuid
from django.db import models
from users.models import User
from .constants import SUBSCRIPTION_TYPES, SUBSCRIPTION_TYPE_DEFAULT
from .constants import APPLICATION_EVENT_DEFAULT, APPLICATION_EVENT_TYPES
from evotor.db import UserId


class Application(models.Model):
    class Meta:
        verbose_name = u'приложение'
        verbose_name_plural = u'приложения'
        db_table = u'applications'

    uuid = models.UUIDField(verbose_name=u'идентификатор приложения', primary_key=True,
                            unique=False, null=False, default=uuid.uuid4)
    name = models.CharField(verbose_name=u'наименование приложения', max_length=100,
                            unique=True, null=False)
    version = models.DecimalField(verbose_name=u'версия приложения', null=False, max_digits=4,
                                  decimal_places=2, default=0.1)

    def __unicode__(self):
        return str(self.uuid)

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        self.name = self.name.encode('utf-8')
        super(Application, self).save(*args, **kwargs)  # Call the "real" save() method.


class Subscription(models.Model):
    class Meta:
        verbose_name = u'подписка на приложение'
        verbose_name_plural = u'журнал подписок на приложение'
        db_table = u'subscriptions'

    # Идентификатор подписки.
    # "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
    subscriptionId = models.UUIDField(verbose_name=u'идентификатор подписки', primary_key=True,
                                      default=uuid.uuid4, null=False)

    # Идентификатор приложения.
    # "productId": "c0d01c35-5193-4cc2-9bfb-be20e0679498",
    productId = models.UUIDField(verbose_name=u'идентификатор приложения', default=uuid.uuid4,
                                 unique=True, null=False)

    # Идентификатор пользователя в Облаке Эвотор.
    # "userId": "01-000000000000001",
    userId = models.ForeignKey(User, verbose_name=u'идентификатор пользователя в Облаке Эвотор',
                               null=False, on_delete=models.CASCADE, default=1)

    # Дата и время отправки события. В соответствовии с ISO 8601.
    # "timestamp": "2017-04-20T18:26:37.753+0000",
    timestamp = UnixDateTimeField(verbose_name=u'дата и время отправки события')

    # Номер события в последовательности. Номер непрерывно возрастает начиная с единицы.
    # Необходим для соблюдения порядка обработки событий.
    # Номер события уникален в рамках подписки (subscriptionId),
    # таким образом, при переустановке приложения номерация событий начнётся сначала
    # "sequenceNumber": 4
    sequenceNumber = models.IntegerField(verbose_name=u'номер события в последовательности', null=False)

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
    # "type": "SubscriptionCreated"
    type = models.CharField(verbose_name=u'тип события', max_length=40, choices=SUBSCRIPTION_TYPES,
                            default=SUBSCRIPTION_TYPE_DEFAULT)

    # Идентификатор тарифа, который вы создаёте на портале разработчиков.
    # "planId": "example"
    planId = models.CharField(verbose_name=u'идентификатор тарифа', max_length=30, default="", null=True)

    # Строка вида PnDT, где n – количество дней бесплатного периода, доступных пользователю в момент активации тарифа.
    # "trialPeriodDuration": "P14DT"
    trialPeriodDuration = models.CharField(verbose_name=u'количество дней бесплатного периода', max_length=5,
                                           default='P07DT')
    # Количество оплаченных устройств.
    # "deviceNumber": 35
    deviceNumber = models.IntegerField(u'количество оплаченных устройств', default=1)

    def __unicode__(self):
        return str(self.subscriptionId)

    def __str__(self):
        return str(self.subscriptionId)


class InstallationEvent(models.Model):
    class Meta:
        verbose_name = u'событие установки приложения'
        verbose_name_plural = u'журнал событий установок приложений'
        db_table = u'installation_events'

    # Идентификатор события.
    # "id": "a99fbf70-6307-4acc-b61c-741ee9eef6c0"
    id = models.UUIDField(verbose_name=u'идентификатор события', primary_key=True,
                          default=uuid.uuid4, null=False)

    # Дата и время отправки события, в миллисекундах. В формате unix timestamp.
    # "timestamp": 1504168645290
    timestamp = models.BigIntegerField(verbose_name=u'дата и время отправки события')

    # Версия API, к которой относятся события.
    # "version": 2
    version = models.IntegerField(u'версия API', default=1)

    # Типы событий:
    #
    # ApplicationInstalled – приложение активировано.
    # ApplicationUninstalled – приложение деактивировано.
    # "type": "ApplicationInstalled"
    type = models.CharField(verbose_name=u'тип события', max_length=40, choices=APPLICATION_EVENT_TYPES,
                            default=APPLICATION_EVENT_DEFAULT)

    def __unicode__(self):
        return u'{} {} [{}]'.format(self.timestamp, self.id, self.type)

    def __str__(self):
        return u'{} {} [{}]'.format(self.timestamp, self.id, self.type)


class Installation(models.Model):
    class Meta:
        verbose_name = u'установленное приложение'
        verbose_name_plural = u'установленные приложения'
        db_table = u'installations'

    # Идентификатор приложения в Облаке Эвотор.
    # regex /^[0-9]{2}-[0-9]{15}$/
    # "productId": "string",
    productId = models.ForeignKey(Application, verbose_name=u'идентификатор приложения Эвотор',
                                  default=uuid.uuid4, db_column='product_id',)
    # Идентификатор пользователя в Облаке Эвотор.
    userId = models.ForeignKey(User, verbose_name=u'идентификатор пользователя Эвотор',
                               default=UserId.DEFAULT_USERID, db_column='user_id', null=False)
    # Событие инсталляции
    installationId = models.ForeignKey(InstallationEvent, verbose_name=u'дата и идентификатор события [событие]',
                                       default=None, on_delete=models.CASCADE, null=False)

    def __unicode__(self):
        return u'{}: {}, {}'.format(self.installationId, self.userId, self.productId)

    def __str__(self):
        return u'{}: {}, {}'.format(self.installationId, self.userId, self.productId)

    # def save(self, *args, **kwargs):
    #    print self.productId, self.userId.userId, self.installation.id
    #    # self.productId = self.productId.uuid
    #    self.userId = self.userId
    #    # self.installation = self.installation.id
    #    super(Installation, self).save(*args, **kwargs)  # Call the "real" save() method.
