# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-23 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191019_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d'),
        ),
        migrations.AlterField(
            model_name='token',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0441\u043e\u0437\u0434\u0430\u043d'),
        ),
        migrations.AlterField(
            model_name='token',
            name='key',
            field=models.CharField(max_length=40, verbose_name='\u043a\u043b\u044e\u0447'),
        ),
    ]
