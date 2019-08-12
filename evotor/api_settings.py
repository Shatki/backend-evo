# -*- coding: utf-8 -*-
NORMAL = u'NORMAL'
ALCOHOL_MARKED = u'ALCOHOL_MARKED'
ALCOHOL_NOT_MARKED = u'ALCOHOL_NOT_MARKED'
TOBACCO_MARKED = u'TOBACCO_MARKED'
SERVICE = u'SERVICE'

PRODUCT_TYPE_DEFAULT = NORMAL

PRODUCT_TYPES = (
    (NORMAL, u'обычный'),
    (ALCOHOL_MARKED, u'маркированный алкоголь'),
    (ALCOHOL_NOT_MARKED, u'немаркированный алкоголь'),
    (TOBACCO_MARKED, u'маркированный табак'),
    (SERVICE, u'услуга (доступен на терминалах начиная с прошивки 3.0)'),
)

NO_VAT = u'NO_VAT' 
VAT_10 = u'VAT_10'
VAT_18 = u'VAT_18' 
VAT_0 = u'VAT_0' 
VAT_18_118 = u'VAT_18_118' 
VAT_10_110 = u'VAT_10_110'

TAX_TYPE_DEFAULT = NO_VAT

TAX_TYPES = (
    (NO_VAT, 'НДС не облагается'),
    (VAT_10, 'НДС 10%'),
    (VAT_18, 'НДС 18%'),
    (VAT_0, 'НДС 0%'),
    (VAT_18_118, 'НДС 18/118'),
    (VAT_10_110, 'НДС 10/110'),
)
