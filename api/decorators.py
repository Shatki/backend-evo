# -*- coding: utf-8 -*-
import status
import evotor.settings as settings
from django.utils.translation import ugettext_lazy as _


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end - start))
        return return_value

    return wrapper


def cloud_authorization(func):
    def wrapper(self, request, *args, **kwargs):
        if request.META['HTTP_AUTH'] == settings.HTTP_AUTH_CLOUD:
            return func(self, request, *args, **kwargs) or self.response
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authorization")
            return self.response
    return wrapper


def user_authorization(func):
    # Todo Нужно доделать!!!
    def wrapper(self, request, *args, **kwargs):
        if request.META['HTTP_AUTH'] == settings.HTTP_AUTH_CLOUD:
            return func(self, request, *args, **kwargs) or self.response
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('User token error'),
                                    subject="Authorization")
            return self.response
    return wrapper
