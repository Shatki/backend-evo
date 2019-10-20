# -*- coding: utf-8 -*-
# Токен указывающийся на вкладке интеграция приложения в Облаке Эвотора
AUTH_TOKEN_EVOTOR = '113d539530237fc6797df463ea0c5fbcf12fcd62'
# 4d01c1a301068abca70fb7bd32a370479c511f4c
AUTH_TOKEN_TYPE = b'bearer'
AUTH_TOKEN_EXPIRY_DAYS = 2
AUTH_TOKEN_USER = 'User'
AUTH_TOKEN_CLOUD = 'Cloud'
AUTH_TOKEN_ANONYMOUS = 'Anonymous'


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
