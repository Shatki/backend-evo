# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-31 16:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_auto_20190726_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installation',
            name='data',
        ),
        migrations.AddField(
            model_name='installationdata',
            name='installation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='applications.Installation', verbose_name='\u0441\u043b\u0443\u0436\u0435\u0431\u043d\u0430\u044f \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='installationdata',
            name='productId',
            field=models.ForeignKey(db_column='product_id', default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='applications.Application', verbose_name='\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u042d\u0432\u043e\u0442\u043e\u0440'),
        ),
        migrations.AlterField(
            model_name='installationdata',
            name='userId',
            field=models.ForeignKey(db_column='user_id', default=10000000000000001, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u042d\u0432\u043e\u0442\u043e\u0440'),
        ),
    ]