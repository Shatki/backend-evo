# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.db import models
from evotor.db import UserIdField
from evotor.validators import login, email


@python_2_unicode_compatible
class User(AbstractUser):
    """
        Класс пользователя системы сервисов Эвотор
    """
    # Идентификатор пользователя. 18 символов
    userId = UserIdField(verbose_name=u'идентификатор пользователя Облака', primary_key=True, unique=True, null=False)

    # Имя логина авторизации
    username = models.CharField(verbose_name=u'имя пользователя в системе',
                                unique=True, max_length=30, db_index=True)
    # E-mail
    # email = models.EmailField(verbose_name=u'электронная почта', unique=True, max_length=255, validators=[email])
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
    REQUIRED_FIELDS = ['userId']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = u'users'

    def __unicode__(self):
        return u'%s' % self.username

    def __str__(self):
        return u'%s' % self.username

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return u'%s' % self.first_name

    # def save(self, *args, **kwargs):
    #     super(User, self).save(*args, **kwargs)  # Call the "real" save() method.

    def has_perm(self, perm, obj=None):
        return True

