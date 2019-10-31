# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
import binascii
import os
from django.conf import settings
from django.db import models


@python_2_unicode_compatible
class Token(models.Model):
    """
    The default authorization token model.
    f46b89a5-8e80-4591-b0aa-94551790444b
    """
    key = models.CharField(u"ключ", max_length=40)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(u"создан", auto_now_add=True)
    updated = models.DateTimeField(u"обновлен", auto_now=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        db_table = "tokens"

    # def save(self, *args, **kwargs):
    #     if not self.key:
    #         self.key = self.generate_key()
    #     return super(Token, self).save(*args, **kwargs)
    # @staticmethod
    # def generate_key():
    #     return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.key


@python_2_unicode_compatible
class Log(models.Model):
    """
    The default authorization token model.
    f46b89a5-8e80-4591-b0aa-94551790444b
    """
    request = models.TextField(verbose_name=u"запрос к серверу", max_length=10240, default=None, null=True)
    response = models.TextField(verbose_name=u"ответ сервера", max_length=10240, default=None, null=True)
    headers = models.TextField(verbose_name=u"заголовки", max_length=2048, default=None, null=True)
    status = models.IntegerField(verbose_name=u'статус оствета', default=0)
    datetime = models.DateTimeField(u"дата и время", auto_now_add=True)

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")
        db_table = "logs"

    def __str__(self):
        return u'[%s] [%s]' % (self.datetime, self.status)

    def __unicode__(self):
        return u'[%s] [%s]' % (self.datetime, self.status)
