# -*- coding: utf-8 -*-
import json
import status
from evotor import settings
from django.views.generic.base import View
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _
from django.db import connection, models, transaction
from django.http import JsonResponse, HttpResponse
from users.models import User
from api.models import Token

from jose import jwt
import datetime
from django.contrib.auth import authenticate


class APIResponse(HttpResponse):
    def __init__(self, data=b'', status_code=status.HTTP_200_OK,
                 error_code=None, reason=None, subject=None, **kwargs):
        self.data = data
        self.content = b''
        self.errors = []
        self.status_code = status_code
        if error_code:
            self.add_error(error_code=error_code, reason=reason, subject=subject)
        kwargs.setdefault('content_type', 'application/json')
        super(APIResponse, self).__init__(content=self.content, status=self.status_code, **kwargs)

    def to_json(self):
        self.content = json.dumps(self.data, cls=DjangoJSONEncoder)

    def make_response(self):
        """
        Создание ответа API
        Метод класса для формирования ответа из данных класса
        :return: None
        """
        if len(self.errors) > 0:
            # Если есть ошибки, то формируем ответ с информацией об ошибках
            self.data = {
                "errors": self.errors
            }
            self.status_code = self.status_code
        else:
            # Если ошибок нет, то отправляем нормальный ответ с требуемыми данными
            self.status_code = status.HTTP_200_OK

    def add_error(self, error_code, reason=None, subject=None):
        # Тут алгоритм присвоения статуса кода ответа
        try:
            self.status_code = status.errors[error_code]
        except KeyError as e:
            reason = e.args[0]
            subject = "undefined unit"
            # можно также присвоить значение по умолчанию вместо бросания исключения
            self.status_code = status.HTTP_400_BAD_REQUEST
        self.errors.append({
            "code": error_code,
            # Причина возникновения ошибки
            "reason": reason,
            # Название неизвестного или отсутствующего поля
            "subject": subject
        })
        self.make_response()
        self.to_json()


class APIView(View):
    def __init__(self):
        self.response = APIResponse()
        self.data = None
        super(APIView, self).__init__()

    @staticmethod
    def decode_exception(exception):
        e = exception.args[0].split(': ')
        return e[0] if e[0] is not None else "Unexpected", e[1] if len(e) > 1 else None

    def action(self, data):
        pass

    def get_data(self, field):
        """
        Запрашивает поля с данными из request
        :param field: Запрашиваемое поле
        :return: validated_data
        """
        try:
            field_data = self.data[field]
            # print field_data
            if field_data is None:
                # JSON Поле есть, но оно пустое
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason="missing data",
                                        subject=field,
                                        )
                return None
        except Exception as e:
            # Совсем отсутствует JSON поле
            self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
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
        user = authenticate(username=username, password=password)
        expiry = datetime.date.today() + datetime.timedelta(days=50)
        payload = {
            'username': user.username,
            'expiry': expiry
        }
        token = jwt.encode(payload, 'seKre8', algorithm='HS256')

        try:
            return Token.objects.create(user=user, key=token)
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                           reason=reason,
                           subject=subject or "token")
            return None

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Всю работу с токенами делает миддлварь
            data = 'Мы авторизованы'

        else:
            # Не авторизованный пользователь
            return APIResponse(error_code=status.ERROR_CODE_1006_WRONG_DATA,
                               reason=_('Permission denied.'),
                               subject="Authentication")


"""
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
"""
