# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-22 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_auto_20190718_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(default=b'\xd0\xbc\xd0\xbe\xd0\xb9 \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd', max_length=50, verbose_name='\u0438\u043c\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430'),
        ),
    ]