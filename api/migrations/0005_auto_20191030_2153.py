# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-30 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='headers',
            field=models.CharField(default=1, max_length=10240, verbose_name='\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0438'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='request',
            field=models.CharField(max_length=10240, verbose_name='\u0437\u0430\u043f\u0440\u043e\u0441 \u043a \u0441\u0435\u0440\u0432\u0435\u0440\u0443'),
        ),
        migrations.AlterField(
            model_name='log',
            name='response',
            field=models.CharField(max_length=10240, verbose_name='\u043e\u0442\u0432\u0435\u0442 \u0441\u0435\u0440\u0432\u0435\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.IntegerField(default=0, verbose_name='\u0441\u0442\u0430\u0442\u0443\u0441 \u043e\u0441\u0442\u0432\u0435\u0442\u0430'),
        ),
    ]
