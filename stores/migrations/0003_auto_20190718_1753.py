# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-18 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20190716_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='code',
            field=models.CharField(blank=True, default=None, max_length=15, null=True, verbose_name='\u043a\u043e\u0434 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430'),
        ),
    ]
