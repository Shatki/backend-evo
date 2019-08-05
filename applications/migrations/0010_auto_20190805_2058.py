# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-05 20:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0009_auto_20190805_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='applications.InstallationEvent', verbose_name='uuid \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438 [\u0441\u043e\u0431\u044b\u0442\u0438\u0435]')),
                ('productId', models.ForeignKey(db_column='product_id', default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='applications.Application', verbose_name='\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u042d\u0432\u043e\u0442\u043e\u0440')),
                ('userId', models.ForeignKey(db_column='user_id', default=10000000000000001, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u042d\u0432\u043e\u0442\u043e\u0440')),
            ],
            options={
                'db_table': 'installations',
                'verbose_name': '\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043e\u0447\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435',
                'verbose_name_plural': '\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043e\u0447\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435',
            },
        ),
        migrations.RemoveField(
            model_name='installationdata',
            name='installation',
        ),
        migrations.RemoveField(
            model_name='installationdata',
            name='productId',
        ),
        migrations.RemoveField(
            model_name='installationdata',
            name='userId',
        ),
        migrations.DeleteModel(
            name='InstallationData',
        ),
    ]
