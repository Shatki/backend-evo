# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from evotor.validators import login, email

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
        db_table = u'users'

    # Идентификатор пользователя.
    userId = models.CharField(verbose_name=u'идентификатор пользователя ', max_length=18,
                              default="01-000000000000001", editable=True, unique=True, null=False)

    # Имя логина авторизации
    username = models.CharField(verbose_name=u'имя пользователя в системе', unique=True, max_length=30, db_index=True,
                                validators=[login])
    # Авторизация будет происходить по E-mail
    email = models.EmailField(verbose_name=u'электронная почта', unique=True, max_length=255, validators=[email])
    # Имя - не является обязательным
    first_name = models.CharField(verbose_name=u'имя пользователя', max_length=40, blank=True, null=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(verbose_name=u'фамилия пользователя', max_length=40, blank=True, null=True)

    # Атрибут суперпользователя
    is_admin = models.BooleanField(default=False, null=False)

    date_joined = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'последнее обновление', auto_now=True)

    # логинимся
    USERNAME_FIELD = 'username'
    # обязательное поле
    REQUIRED_FIELDS = ['email', ]

    def __unicode__(self):
        return u'%s' % self.username

    def __str__(self):
        return u'%s' % self.username

    def get_photo(self):
        return self.photo

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.userId = self.userId.encode('utf-8')
        super(User, self).save(*args, **kwargs)  # Call the "real" save() method.

    def has_perm(self, perm, obj=None):
        return True


class Subscription(models.Model):
    class Meta:
        verbose_name = u'подписка на приложение'
        verbose_name_plural = u'подписки на приложение'

    # Идентификатор подписки. "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
    subscriptionId = models.UUIDField(verbose_name=u'идентификатор подписки', primary_key=True,
                                      default=uuid.uuid4, null=False)

    # Идентификатор приложения. "productId": "c0d01x35-5193-4cc2-9bfb-be20e0679498",
    productId = models.UUIDField(verbose_name=u'идентификатор приложения', default=uuid.uuid4,
                                 unique=True, null=False)

    # Идентификатор пользователя в Облаке Эвотор. "userId": "01-000000000000001",
    userId = models.ForeignKey(User, verbose_name=u'идентификатор пользователя в Облаке Эвотор',
                               on_delete=models.CASCADE)

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
    # Идентификатор тарифа, который вы создаёте на портале разработчиков.
    planId = models.UUIDField(verbose_name=u'идентификатор тарифа', default=uuid.uuid4, null=False)

    # "trialPeriodDuration": "P14DT",
    # Строка вида PnDT, где n – количество дней бесплатного периода, доступных пользователю в момент активации тарифа.
    trialPeriodDuration = models.CharField(verbose_name=u'количество дней бесплатного периода', max_length=4,
                                           default='P07DT')
    # Количество оплаченных устройств. "deviceNumber": 35
    deviceNumber = models.IntegerField(u'количество оплаченных устройств', default=1)

    def __str__(self):
        return self.subscriptionId