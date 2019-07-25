# -*- coding: utf-8 -*-
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
