# -*- coding: utf-8 -*-
import json

import status
from evotor import settings
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, models, transaction
from django.http import JsonResponse

from users.models import User, Token


class APIResponse(View):
    evotor_token = settings.EVOTOR_TOKEN
    evotor_type_token = u'Bearer'

    @staticmethod
    def response(message, http_status):
        return csrf_exempt(JsonResponse(
            # неверный токен облака Эвотор.
            message, status=http_status))

    def action(self, data):
        return data, status.HTTP_200_OK

    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            try:
                token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            except:
                return self.response({
                    # неверный токен облака Эвотор.
                    'errors': '1001'},
                    status.HTTP_409_CONFLICT)
            if token[0] == self.evotor_type_token and token[1] == self.evotor_token:
                data = json.loads(request.body.decode("utf-8"))
                # hasBilling: boolean (Required)
                # Определяет, на чьей стороне производится биллинг по данному пользователю.
                #
                # true - в стороннем сервисе
                #
                # false - на стороне Эвотор
                message, http_status = self.action(data)
                return self.response(message, http_status)
            else:
                return self.response({
                    # неверный тип токена, нужен 'Bearer'
                    'errors': '1001'
                }, status.HTTP_401_UNAUTHORIZED)

        else:
            return self.response({
                # Метод не POST
                'errors': 'Разрешен только POST запрос'
            }, status.HTTP_400_BAD_REQUEST)

    @classmethod
    def as_view(cls, **initkwargs):
        """
        Store the original class on the view function.

        This allows us to discover information about the view when we do URL
        reverse lookups.  Used for breadcrumb generation.
        """
        view = super(APIResponse, cls).as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        # Note: session based authentication is explicitly CSRF validated,
        # all other authentication is CSRF exempt.
        return csrf_exempt(view)
