# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from evotor.validators import login, email


class User(AbstractUser):
    class Meta:
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'
        db_table = u'users'

    # Идентификатор пользователя. 18 символов
    userId = models.BigIntegerField(verbose_name=u'идентификатор пользователя ', primary_key=True,
                                    default=1000000000000001, editable=True, unique=True, null=False)

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
        return u'%s' % self.userId

    def __str__(self):
        id = (('000000000000000' + str(self.userId))[-15:])
        return u'01-{}'.format(self.userId)

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.userId = self.userId.encode('utf-8')
        super(User, self).save(*args, **kwargs)  # Call the "real" save() method.

    def has_perm(self, perm, obj=None):
        return True

