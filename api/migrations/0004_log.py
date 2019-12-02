# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-30 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191023_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.CharField(max_length=10240, verbose_name='\u0417\u0430\u043f\u0440\u043e\u0441')),
                ('response', models.CharField(max_length=10240, verbose_name='\u041e\u0442\u0432\u0435\u0442')),
                ('status', models.IntegerField(verbose_name='\u0441\u0442\u0430\u0442\u0443\u0441 \u043e\u0441\u0442\u0432\u0435\u0442\u0430')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u0434\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f')),
            ],
            options={
                'db_table': 'logs',
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
