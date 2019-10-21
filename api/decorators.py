# -*- coding: utf-8 -*-
import status
import evotor.settings as settings


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
        if request.META['AUTH_TOKEN'] == settings.AUTH_TOKEN_CLOUD:
            return func(self, request, *args, **kwargs) or self.response
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authentication")
            return self.response
    return wrapper
