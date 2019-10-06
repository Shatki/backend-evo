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
        self.evotor_type_token = 'bearer'
        self.evotor_token = settings.EVOTOR_TOKEN
        self.errors = []
        self._status = status.HTTP_200_OK
        self._data = []
        super(APIResponse, self).__init__()

    def response(self, message=None):
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

    @staticmethod
    def decode_exception(exception):
        e = exception.args[0].split(': ')
        return e[0] if e[0] is not None else "Unexpected", e[1] if len(e) > 1 else None

    def add_error(self, code, reason=None, subject=None):
        # Тут алгоритм присвоения статуса кода ответа
        try:
            self._status = status.errors[code]
        except KeyError as e:
            reason = e.args[0]
            subject = "undefined unit"
            # можно также присвоить значение по умолчанию вместо бросания исключения
            self._status = status.HTTP_400_BAD_REQUEST

        self.errors.append({
            "code": code,
            # Причина возникновения ошибки
            "reason": reason,
            # Название неизвестного или отсутствующего поля
            "subject": subject
        })

    def action(self, data):
        pass

    def get_data(self, field):
        """
        :param field: Запрашиваемое поле
        :return: validated_data
        """
        try:
            field_data = self._data[field]
            if field_data is None:
                # JSON Поле есть, но оно пустое
                self.add_error(status.ERROR_CODE_2002_FIELDS_ERROR,
                               reason="missing data",
                               subject=field,
                               )
                return None
        except Exception as e:
            # Совсем отсутствует JSON поле
            self.add_error(status.ERROR_CODE_2002_FIELDS_ERROR,
                           reason="missing field",
                           subject=e.args[0],
                           )
            return None
        else:
            return field_data

    def get_token(self, user):
        try:
            return Token.objects.get(user=user)
        except Exception as e:
            reason, subject = self.decode_exception(e)
            # эту ошибку нужно записать в логи
            self.add_error(status.ERROR_CODE_3000_DB_ERROR,
                           reason=reason,
                           subject=subject or "db")
            return None

    def create_token(self, user):
        try:
            return Token.objects.create(user=user)
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                           reason=reason,
                           subject=subject or "token")
            return None

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                token = request.META.get('HTTP_AUTHORIZATION').split(" ")
            except Exception as e:
                self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                               reason=e.args[0],
                               subject="token")
                return self.response()
            # Проверяем наличие перед токеном типа
            if len(token) != 2 or token[0].lower() != self.evotor_type_token:
                self.add_error(status.ERROR_CODE_2001_SYNTAX_ERROR,
                               reason="unknown type. Example: 'Bearer evotor_token'",
                               subject="token")
                return self.response()

            if token[1] == self.evotor_token:
                try:
                    self._data = json.loads(request.body.decode("utf-8"))
                except ValueError as e:
                    self.add_error(status.ERROR_CODE_2001_SYNTAX_ERROR,
                                   reason=e.args[0],
                                   subject="JSON request")
                    return self.response()
                # Вызываем основное действие
                return self.response(self.action(self._data))
            else:
                # Не верный токен?
                self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN)
                return self.response()
        else:
            self.add_error(status.ERROR_CODE_2001_SYNTAX_ERROR)
            return self.response()
