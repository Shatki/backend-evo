# -*- coding: utf-8 -*-
# 4d01c1a301068abca70fb7bd32a370479c511f4c
AUTH_TOKEN_TYPE = b'bearer'
AUTH_TOKEN_REGEX = '/^[a-zA-Z0-9_=-]+$/'
# AUTH_USERNAME_REGEX = '/^((8|\+7)[\-]?)?(\(?\d{3}\)?[\-]?)?[\d\-]{7,10}$/'

AUTH_TOKEN_EXPIRY_DAYS = 2

HTTP_AUTH_USER = 'User'
HTTP_AUTH_CLOUD = 'Cloud'
HTTP_AUTH_ANONYMOUS = 'Anonymous'

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
VAT_20 = u'VAT_20'
VAT_0 = u'VAT_0'
VAT_20_120 = u'VAT_20_120'
VAT_10_110 = u'VAT_10_110'

TAX_TYPE_DEFAULT = NO_VAT

TAX_TYPES = (
    (NO_VAT, 'Без НДС'),
    (VAT_10, 'НДС 10%'),
    (VAT_20, 'НДС 20%'),
    (VAT_0, 'НДС 0%'),
    (VAT_20_120, 'НДС 20/120'),
    (VAT_10_110, 'НДС 10/110'),
)

MEASURE_TYPE_DEFAULT = u'шт'


SUBSCRIPTION_CREATED = u'SubscriptionCreated'
ADDONS_UPDATED = u'AddonsUpdated'
SUBSCRIPTION_ACTIVATED = u'SubscriptionActivated'
SUBSCRIPTION_RENEWED = u'SubscriptionRenewed'
SUBSCRIPTION_TERMS_CHANGED = u'SubscriptionTermsChanged'
SUBSCRIPTION_TERMINATION_REQUESTED = u'SubscriptionTerminationRequested'
SUBSCRIPTION_TERMINATED = u'SubscriptionTerminated'

SUBSCRIPTION_TYPE_DEFAULT = SUBSCRIPTION_CREATED

SUBSCRIPTION_TYPES = {
    (SUBSCRIPTION_CREATED, u'новая подписка'),
    (ADDONS_UPDATED, u'список платных опций, выбранных пользователем'),
    (SUBSCRIPTION_ACTIVATED, u'подписка активирована'),
    (SUBSCRIPTION_RENEWED, u'подписка продлена на следующий период'),
    (SUBSCRIPTION_TERMS_CHANGED, u'изменились условия подписки'),
    (SUBSCRIPTION_TERMINATION_REQUESTED, u'запрос на завершение подписки'),
    (SUBSCRIPTION_TERMINATED, u'подписка завершена')
}

APPLICATION_EVENT_INSTALLED = u'ApplicationInstalled'
APPLICATION_EVENT_UNINSTALLED = u'ApplicationUninstalled'
APPLICATION_EVENT_DEFAULT = APPLICATION_EVENT_INSTALLED

APPLICATION_EVENT_TYPES = {
    (APPLICATION_EVENT_INSTALLED, u'приложение установлено'),
    (APPLICATION_EVENT_UNINSTALLED, u'приложение удалено'),
}
