# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-20 10:42
from __future__ import unicode_literals

from django.db import migrations
import evotor.db


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0025_auto_20190913_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='timestamp',
            field=evotor.db.TimestampField(verbose_name='\u0434\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 \u0441\u043e\u0431\u044b\u0442\u0438\u044f'),
        ),
    ]
