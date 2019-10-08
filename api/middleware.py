# -*- coding: utf-8 -*-
from evotor import settings
from django.http import HttpResponseBadRequest
from django.contrib import auth


class TokenMiddleware(object):
    """
        Миддлварь, которая авторизует пользователя по токену в заголовке 'HTTP_AUTHORIZATION'
    """
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', b'').split()

        if not auth_header or auth_header[0].lower() != settings.AUTH_TOKEN_TYPE:
            return None

        # If they specified an invalid token, let them know.
        if len(auth_header) != 2:
            return HttpResponseBadRequest("Improperly formatted token")

        user = auth.authenticate(token=auth_header[1])
        if user:
            request.user = user