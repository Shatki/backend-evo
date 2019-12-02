# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-28 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190714_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlcoCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='0123456789123456789', max_length=19, unique=True, verbose_name='\u0448\u0442\u0440\u0438\u0445\u043a\u043e\u0434')),
            ],
            options={
                'db_table': 'alcocodes',
                'verbose_name': '\u0430\u043b\u043a\u043e\u043a\u043e\u0434',
                'verbose_name_plural': '\u0430\u043b\u043a\u043e\u043a\u043e\u0434\u044b',
            },
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='\u0448\u0442', max_length=15, unique=True, verbose_name='\u0435\u0434\u0438\u043d\u0430\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f')),
            ],
            options={
                'db_table': 'measures',
                'verbose_name': '\u0435\u0434\u0438\u043d\u0430\u0446\u0430',
                'verbose_name_plural': '\u0435\u0434\u0438\u043d\u0438\u0446\u044b',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='barCodes',
        ),
        migrations.AddField(
            model_name='barcode',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='alcoholByVolume',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=5, verbose_name='\u043a\u0440\u0435\u043f\u043a\u043e\u0441\u0442\u044c \u0430\u043b\u043a\u043e\u0433\u043e\u043b\u044c\u043d\u043e\u0438\u0306 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438'),
        ),
        migrations.AddField(
            model_name='product',
            name='alcoholProductKindCode',
            field=models.IntegerField(default=None, verbose_name='\u043a\u043e\u0434 \u0432\u0438\u0434\u0430 \u0430\u043b\u043a\u043e\u0433\u043e\u043b\u044c\u043d\u043e\u0438\u0306 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0424\u0421\u0420\u0410\u0420'),
        ),
        migrations.AddField(
            model_name='product',
            name='tareVolume',
            field=models.DecimalField(decimal_places=3, default=None, max_digits=6, verbose_name='\u0451\u043c\u043a\u043e\u0441\u0442\u044c \u0442\u0430\u0440\u044b \u0430\u043b\u043a\u043e\u0433\u043e\u043b\u044c\u043d\u043e\u0439 \u043f\u0440\u043e\u0434\u0443\u043a\u0446\u0438\u0438 \u0432 \u043b\u0438\u0442\u0440\u0430\u0445'),
        ),
        migrations.AlterField(
            model_name='barcode',
            name='code',
            field=models.CharField(default='0123456789101', max_length=30, unique=True, verbose_name='\u0448\u0442\u0440\u0438\u0445\u043a\u043e\u0434'),
        ),
        migrations.AlterField(
            model_name='product',
            name='articleNumber',
            field=models.CharField(blank=True, max_length=20, verbose_name='\u0430\u0440\u0442\u0438\u043a\u0443\u043b \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, max_length=10, verbose_name='\u041a\u043e\u0434 \u0442\u043e\u0432\u0430\u0440\u0430 \u0438\u043b\u0438 \u0433\u0440\u0443\u043f\u043f\u044b \u0442\u043e\u0432\u0430\u0440\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=100, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='product',
            name='measureName',
            field=models.ForeignKey(blank=True, default='\u0448\u0442', on_delete=django.db.models.deletion.CASCADE, to='products.Measure', verbose_name='\u0435\u0434\u0438\u043d\u0438\u0446\u0430 \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='product',
            name='parentUuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='\u043f\u0440\u0438\u043d\u0430\u0434\u043b\u0435\u0436\u043d\u043e\u0441\u0442\u044c \u043a \u0433\u0440\u0443\u043f\u043f\u0435 \u0442\u043e\u0432\u0430\u0440\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax',
            field=models.CharField(choices=[('NO_VAT', b'\xd0\x91\xd0\xb5\xd0\xb7 \xd0\x9d\xd0\x94\xd0\xa1'), ('VAT_10', b'\xd0\x9d\xd0\x94\xd0\xa1 10%'), ('VAT_20', b'\xd0\x9d\xd0\x94\xd0\xa1 20%'), ('VAT_0', b'\xd0\x9d\xd0\x94\xd0\xa1 0%'), ('VAT_20_120', b'\xd0\x9d\xd0\x94\xd0\xa1 20/120'), ('VAT_10_110', b'\xd0\x9d\xd0\x94\xd0\xa1 10/110')], default='NO_VAT', max_length=10, verbose_name='c\u0442\u0430\u0432\u043a\u0430 \u041d\u0414\u0421 \u0434\u043b\u044f \u0442\u043e\u0432\u0430\u0440\u0430'),
        ),
    ]