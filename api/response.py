# -*- coding: utf-8 -*-
import json
from functools import update_wrapper

from django.utils.decorators import classonlymethod

import status
from evotor import settings
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, models, transaction
from django.http import JsonResponse, HttpResponse

from users.models import User, Token


class APIResponse(View):
    def __init__(self):
        self.evotor_type_token = 'Bearer'
        self.evotor_token = settings.EVOTOR_TOKEN
        self.errors = []
        self._status = status.HTTP_200_OK
        super(APIResponse, self).__init__()

    def response(self, message):
        if len(self.errors) > 0:
            return JsonResponse(
                # неверный токен облака Эвотор.
                {
                    "errors": self.errors
                },
                status=self._status,
                safe=False)
        else:
            return JsonResponse(
                # неверный токен облака Эвотор.
                message,
                status=status.HTTP_200_OK,
                safe=False)

    def add_error(self, code, reason=None, subject=None):
        self.errors.append({
            "code": code,
            "reason": reason,
            "subject": subject
        })
        # Тут алгоритм присвоения статуса кода ответа
        if code == status.ERROR_CODE_1001_WRONG_TOKEN:
            self._status = status.HTTP_401_UNAUTHORIZED
        elif code == status.ERROR_CODE_1006_WRONG_DATA:
            self._status = status.HTTP_401_UNAUTHORIZED
        elif code == status.ERROR_CODE_2004_USER_EXIST:
            self._status = status.HTTP_409_CONFLICT
        else:
            self._status = status.HTTP_400_BAD_REQUEST

    def action(self, data):
        pass

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            except:
                self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN)
                return self.response({})
            if token[0] == self.evotor_type_token and token[1] == self.evotor_token:
                data = json.loads(request.body.decode("utf-8"))
                # hasBilling: boolean (Required)
                # Определяет, на чьей стороне производится биллинг по данному пользователю.
                #
                # true - в стороннем сервисе
                #
                # false - на стороне Эвотор

                # Все удачно, - возвращаем ответ 200
                return self.response(self.action(data))
            else:
                # Возможно не Bearer?
                self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN)
                return self.response({})

                # errors.add(status.ERROR_CODE_1001_WRONG_TOKEN)
                # return self.response()
        else:
            self.add_error(status.ERROR_CODE_2002_BAD_REQUEST)
            return self.response({})
