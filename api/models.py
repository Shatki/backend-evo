# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from evotor.db import UserIdField, UserId
from django.db import models
from stores.models import Store


# Create your models here.
class UserEvotor(models.Model):
    """
        Класс пользователя облака Эвотор
    """
    class Meta:
        verbose_name = u'пользователь облака Эвотор'
        verbose_name_plural = u'пользователи облака Эвотор'
        db_table = u'users'
    # Идентификатор пользователя. 18 символов
    userId = UserIdField(verbose_name=u'идентификатор пользователя ', primary_key=True,
                         unique=True, null=False)
    # stores = models.ManyToManyField(Store, verbose_name=u'магазины пользователя')
    date_joined = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'последнее обновление', auto_now=True)

    def __unicode__(self):
        return u'%s' % self.userId

    def __str__(self):
        return u'%s' % self.userId

    def has_perm(self, perm, obj=None):
        return True