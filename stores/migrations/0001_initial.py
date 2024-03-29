# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-14 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('address', models.CharField(max_length=100, null=True, verbose_name='\u0430\u0434\u0440\u0435\u0441 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430')),
                ('name', models.CharField(default='\u043c\u043e\u0439 \u043c\u0430\u0433\u0430\u0437\u0438\u043d', max_length=50, verbose_name='\u0438\u043c\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430')),
                ('code', models.CharField(blank=True, default='null', max_length=15, verbose_name='\u043a\u043e\u0434 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430')),
            ],
            options={
                'db_table': 'stores',
                'verbose_name': '\u043c\u0430\u0433\u0430\u0437\u0438\u043d',
                'verbose_name_plural': '\u043c\u0430\u0433\u0430\u0437\u0438\u043d\u044b',
            },
        ),
    ]
