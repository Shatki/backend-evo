# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import uuid
from evotor.settings import PRODUCT_TYPES, PRODUCT_TYPE_DEFAULT
from evotor.settings import TAX_TYPES, TAX_TYPE_DEFAULT, MEASURE_TYPE_DEFAULT
from django.db import models
from users.models import User


# Create your models here.
@python_2_unicode_compatible
class Measure(models.Model):
    class Meta:
        verbose_name = u'единаца'
        verbose_name_plural = 'единицы'
        db_table = 'measures'

    name = models.CharField(verbose_name=u'единаца измерения', max_length=15,
                            default=MEASURE_TYPE_DEFAULT, blank=False, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name


@python_2_unicode_compatible
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
    # Массив штрихкодов товара. "barCodes": [], EAN-13: 123456789102
    code = models.CharField(verbose_name=u'штрихкод', max_length=30,
                            default='0123456789101', blank=False, unique=True)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return u'%s' % self.code


@python_2_unicode_compatible
class AlcoCode(models.Model):
    class Meta:
        verbose_name = u'алкокод'
        verbose_name_plural = 'алкокоды'
        db_table = 'alcocodes'

    code = models.CharField(verbose_name=u'штрихкод', max_length=19,
                            default='0123456789123456789', blank=False, unique=True)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return u'%s' % self.code


@python_2_unicode_compatible
class Product(models.Model):
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = 'товары'
        db_table = 'products'

    # Идентификатор товара или группы товаров, уникальный в рамках магазина.
    # "uuid": "01ba18b6-8707-5f47-3d9c-4db058054cb2",
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, null=False)

    # Название товара или группы товаров.
    # "name": "Сидр",
    name = models.CharField(verbose_name=u'название товара или группы товаров',
                            max_length=100, blank=False, null=False)

    # Указывает является элемент товаром или группой товаров:
    # "group": false,
    group = models.BooleanField(verbose_name=u'является группой', null=False)

    # Уникальный идентификатор группы, к которой принадлежит товар или группа товаров.
    # "parentUuid": "1ddea16b-971b-dee5-3798-1b29a7aa2e27",
    parentUuid = models.ForeignKey('self', verbose_name=u'принадлежность к группе товаров',
                                   blank=False)

    # Тип товара:
    #
    # NORMAL – обычный;
    # ALCOHOL_MARKED – маркированный алкоголь;
    # ALCOHOL_NOT_MARKED – немаркированный алкоголь;
    # TOBACCO_MARKED – маркированный табак;
    # SERVICE – услуга (доступен на терминалах начиная с прошивки 3.0).
    # "type": "ALCOHOL_NOT_MARKED",
    type = models.CharField(verbose_name=u'тип товара', max_length=20,
                            blank=False, default=PRODUCT_TYPE_DEFAULT, choices=PRODUCT_TYPES)

    # Количество товара в наличии (остаток). До семи знаков в целой и трёх знаков в дробной части.
    # "quantity": 12,
    quantity = models.DecimalField(verbose_name=u'количество товара в наличии',
                                   max_digits=10, decimal_places=3)

    # Единица измерения товара.
    # "measureName": "шт",
    measureName = models.ForeignKey(Measure, verbose_name=u'единица измерения товара',
                                    default=MEASURE_TYPE_DEFAULT, blank=True)
    # Ставка НДС для товара.
    # "tax": "VAT_18",
    tax = models.CharField(verbose_name=u'cтавка НДС для товара', max_length=10,
                           blank=False, default=TAX_TYPE_DEFAULT, choices=TAX_TYPES)

    # Отпускная цена товара.
    # "price": 123.12,
    price = models.DecimalField(verbose_name=u'отпускная цена товара', default=0.00,
                                max_digits=9, decimal_places=2)

    # Указывает можно добавить товар в чек или нельзя.
    # "allowToSell": true,
    allowToSell = models.BooleanField(verbose_name=u'разрешение на продажу товара', default=True)

    # Закупочная цена товара.
    # "costPrice": 100.123,
    costPrice = models.DecimalField(verbose_name=u'закупочная цена товара', default=0.00,
                                    max_digits=9, decimal_places=2)

    # Описание товара.
    # "description": "Вкусный яблочный сидр.",
    description = models.CharField(verbose_name=u"описание товара", max_length=100, blank=True)

    # Артикул товара.
    # "articleNumber": "сид123",
    articleNumber = models.CharField(verbose_name=u'артикул товара',
                                     max_length=20, blank=True)

    # Код товара или группы товаров.
    # "code": "6",
    code = models.CharField(verbose_name=u'Код товара или группы товаров',
                            blank=True, max_length=10)

    # Массив штрихкодов товара. (Переместили с отдельную модель)
    # "barCodes": [], EAN-13: 123456789102
    barCodes = models.ManyToManyField(BarCode, verbose_name=u'штрихкоды', symmetrical=False, through="BarCodes")

    # Массив строк кодов алкогольной продукции ЕГАИС. (Переместили с отдельную модель)
    # "alcoCodes": []
    alcoCodes = models.ManyToManyField(AlcoCode, verbose_name=u'Алкокоды', symmetrical=False, through="AlcoCodes")

    # Крепость алкогольной продукции.
    # До трёх знаков в дробной части. Для алкогольных товаров значение может быть в диапазоне от 0.001 до 99.999.
    # Поле передаётся только если group = false.
    # "alcoholByVolume": 5.45
    alcoholByVolume = models.DecimalField(verbose_name=u'крепкость алкогольной продукции', default=None,
                                          max_digits=5, decimal_places=3)

    # Код вида алкогольной продукции ФСРАР.
    # Для алкогольных товаров значение может быть в диапазоне от 1 до 999.
    # Поле передаётся только если group = false.
    # "alcoholProductKindCode": 123,
    alcoholProductKindCode = models.IntegerField(verbose_name=u'код вида алкогольной продукции ФСРАР', default=None)

    # Ёмкость тары алкогольной продукции в литрах. До трёх знаков в дробной части.
    # Для алкоголя значение может быть диапазоне от 0.001 до 999.999.
    # Поле передаётся только если group = false.
    # "tareVolume": 0.57
    tareVolume = models.DecimalField(verbose_name=u'ёмкость тары алкогольной продукции в литрах', default=None,
                                     max_digits=6, decimal_places=3)

    # user = models.ForeignKey(User, verbose_name=u'пользователь')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.name


class BarCodes(models.Model):
    class Meta:
        verbose_name = u'штрихкод'
        verbose_name_plural = u'штрихкоды'
        db_table = 'barcodes_table'

    barcode = models.ForeignKey(BarCode, related_name="barcodes_code")
    product = models.ForeignKey(Product, related_name="barcodes_product")


class AlcoCodes(models.Model):
    class Meta:
        verbose_name = u'алкокод'
        verbose_name_plural = u'алкокодкоды'
        db_table = 'alcocodes_table'

    alcocode = models.ForeignKey(AlcoCode, related_name="alcocodes_code")
    product = models.ForeignKey(Product, related_name="alcocodes_product")

