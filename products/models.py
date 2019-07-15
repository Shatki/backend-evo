# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from evotor.settings import PRODUCT_TYPES, PRODUCT_TYPE_DEFAULT
from evotor.settings import TAX_TYPES, TAX_TYPE_DEFAULT
from django.db import models


# Create your models here.
class BarCode(models.Model):
    class Meta:
        verbose_name = u'штрихкод'
        verbose_name_plural = 'штрихкоды'
        db_table = 'barcodes'

    # formats = {
    #     '0x1FFL': "OneD",
    #     '0x1L': "CODE_39",
    #     '0x2L': "CODE_128",
    #     '0x4L': "CODE_93",
    #     '0x8L': "CODABAR",
    #     '0x10L': "ITF",
    #     '0x20L': "EAN_13",
    #     '0x40L': "EAN_8",
    #     '0x80L': "UPC_A",
    #     '0x100L': "UPC_E",
    # }
    code = models.CharField(primary_key=True, verbose_name=u'штрихкод', max_length=20,
                            default='0123456789101', blank=False, unique=True)

    def __str__(self):
        return self.code


class Product(models.Model):
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = 'товары'
        db_table = 'products'

    # Идентификатор товара или группы товаров, уникальный в рамках магазина.
    # "uuid": "01ba18b6-8707-5f47-3d9c-4db058054cb2",
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)

    # Название товара или группы товаров. "name": "Сидр",
    name = models.CharField(verbose_name=u'название товара или группы товаров',
                            max_length=100, blank=False, null=False)

    # Указывает является элемент товаром или группой товаров: "group": false,
    group = models.BooleanField(verbose_name=u'является группой', null=False)

    # Уникальный идентификатор группы, к которой принадлежит товар или группа товаров.
    # "parentUuid": "1ddea16b-971b-dee5-3798-1b29a7aa2e27",
    parentUuid = models.ForeignKey('self', verbose_name=u'принадлежность к группе товаров',
                                   blank=False, null=True)

    # Тип товара:
    #
    # NORMAL – обычный;
    # ALCOHOL_MARKED – маркированный алкоголь;
    # ALCOHOL_NOT_MARKED – немаркированный алкоголь;
    # TOBACCO_MARKED – маркированный табак;
    # SERVICE – услуга (доступен на терминалах начиная с прошивки 3.0).
    # "type": "ALCOHOL_NOT_MARKED",
    type = models.CharField(verbose_name=u'тип товара', max_length=20,
                            null=False, blank=False, default=PRODUCT_TYPE_DEFAULT, choices=PRODUCT_TYPES)

    # Количество товара в наличии (остаток). До семи знаков в целой и трёх знаков в дробной части.
    # "quantity": 12,
    quantity = models.DecimalField(verbose_name=u'количество товара в наличии', null=False,
                                   max_digits=10, decimal_places=3)

    # Единица измерения товара. "measureName": "шт",
    measureName = models.CharField(verbose_name=u'единица измерения товара', max_length=15,
                                   default=u'шт', blank=True, null=False)
    # Ставка НДС для товара. "tax": "VAT_18",
    tax = models.CharField(verbose_name=u'cтавка НДС для товара', max_length=10,
                           null=False, blank=False, default=TAX_TYPE_DEFAULT, choices=TAX_TYPES)

    # Отпускная цена товара. "price": 123.12,
    price = models.DecimalField(verbose_name=u'отпускная цена товара', null=False, default=0.00,
                                max_digits=9, decimal_places=2)

    # Указывает можно добавить товар в чек или нельзя. "allowToSell": true,
    allowToSell = models.BooleanField(verbose_name=u'разрешение на продажу товара',
                                      null=False, default=True)

    # Закупочная цена товара."costPrice": 100.123,
    costPrice = models.DecimalField(verbose_name=u'закупочная цена товара', null=False, default=0.00,
                                    max_digits=9, decimal_places=2)

    # Описание товара. "description": "Вкусный яблочный сидр.",
    description = models.CharField(verbose_name=u"описание товара", max_length=100, blank=True, null=True)

    # Артикул товара. "articleNumber": "сид123",
    articleNumber = models.CharField(verbose_name=u'артикул товара',
                                     max_length=20, blank=True, null=True)

    # Код товара или группы товаров. "code": "6",
    code = models.CharField(verbose_name=u'Код товара или группы товаров',
                            blank=True, max_length=10, null=True)

    # Массив штрихкодов товара. "barCodes": [], EAN-13: 123456789102
    barCodes = models.ManyToManyField(BarCode, verbose_name=u'штрихкоды', symmetrical=None)

    # "alcoCodes": [],
    # "alcoholByVolume": 5.45,
    # "alcoholProductKindCode": 123,
    # "tareVolume": 0.57

    def __str__(self):
        return self.name
