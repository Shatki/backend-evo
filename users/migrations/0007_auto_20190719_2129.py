# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-19 21:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190719_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='userId',
        ),
    ]
