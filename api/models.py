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
