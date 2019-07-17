# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models


# Create your models here.
class Store(models.Model):
    class Meta:
        verbose_name = u'магазин'
        verbose_name_plural = u'магазины'
        db_table = 'stores'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)
    address = models.CharField(verbose_name=u'адрес магазина', max_length=100, null=True)
    name = models.CharField(verbose_name=u'имя магазина', max_length=50, null=False, default=u'мой магазин')
    code = models.CharField(verbose_name=u'код магазина', max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.encode('utf-8')
        self.address = self.address.encode('utf-8')
        super(Store, self).save(*args, **kwargs)  # Call the "real" save() method.


