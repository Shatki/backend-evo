# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json
from api.crypto import encrypt, decrypt
import evotor.settings as settings

from django.utils.translation import ugettext_lazy as _
from .response import APIView, status
from users.models import User
from api.models import Token
from applications.models import Subscription, InstallationEvent, Installation
from stores.models import Store


class UserCreateView(APIView):
    """
        Регистрация учетной записи пользователя
        Создание нового пользователя и токена доступа
            Запрос:
            >{
                "userId": "01-000000000000003",
                *"password": "password",
                *"username": "test3",
                "customField": "Дополнительные данные о пользователе"
            }
            Ответ:
            >{
                "token": "TLWHR7jA7HzBDmoRzUpHteNyDPqAkOAc/DP81JuM0dXpq8h60X+W0jh+PEWe1jkmJq/C6iW6YYafYzVGxhM3PABuDgTHX3QMeUcVUYRB9K39y7WKxISibx5FSm4Ek8Ek",
                "userId": "01-000000000000004"
                }
                2-х дневный
        """
    def post(self, request, *args, **kwargs):
        if request.META['AUTH_TOKEN'] == settings.AUTH_TOKEN_CLOUD:
            # Получаем и преобразуем данные из request.body в JSON
            try:
                self.data = json.loads(request.body.decode(settings.CODING))
            except ValueError as e:
                # reason, subject = self.decode_exception(e)
                self.response.add_error(error_code=status.ERROR_CODE_2001_SYNTAX_ERROR,
                                        reason=_(e.args[0]),
                                        subject="JSON")
                # Вернем ошибки
                return self.response

            # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
            self.userId = self.get_data('userId')
            self.password = self.get_data('password')
            self.username = self.get_data('username')
            if self.userId is None or self.password is None or self.username is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Permission denied.'),
                                        subject="Authentication")
                # Вернем ошибки
                return self.response

            # Создаем нового пользователя
            try:
                user = User.objects.create(userId=self.userId, username=self.username)
            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_2005_USER_EXIST,
                                        reason=reason,
                                        subject=subject or "user")
                # Вернем ошибки
                return self.response
            else:
                user.set_password(self.password)
                user.save()

                expiry = str(datetime.date.today() + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_DAYS))
                payload = json.dumps({'id': user.userId, 'usrnm': user.username, 'exp': expiry})
                token = encrypt(payload, settings.SECRET_KEY)

                # Все удачно вернем данные
                self.response.data = {
                    "userId": user.userId,
                    "token": token
                }
                self.response.to_json()
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authentication")
        return self.response


class UserVerifyView(APIView):
    """
    Авторизация пользователя:
        Запрос:
        >{
            "userId": "01-000000000000004",
            "password": "password",
            "username": "test4"
        }
        Ответ:
        >{
            "userId": "01-000000000000003",
            "token": "toaWaep4chou7ahkoogiu9Iusaht9ima"
        }
    """
    def post(self, request, *args, **kwargs):
        if request.META['AUTH_TOKEN'] == settings.AUTH_TOKEN_CLOUD:
            # Получаем и преобразуем данные из request.body в JSON
            try:
                self.data = json.loads(request.body.decode(settings.CODING))
            except ValueError as e:
                # reason, subject = self.decode_exception(e)
                self.response.add_error(error_code=status.ERROR_CODE_2001_SYNTAX_ERROR,
                                        reason=_(e.args[0]),
                                        subject="JSON")
                # Вернем ошибки
                return self.response

            # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
            self.userId = self.get_data('userId')
            self.password = self.get_data('password')
            self.username = self.get_data('username')
            if self.userId is None or self.password is None or self.username is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Permission denied.'),
                                        subject="Authentication")
                # Вернем ошибки
                return self.response

            # Создаем нового пользователя
            try:
                user = User.objects.create(userId=self.userId, username=self.username)
            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_2005_USER_EXIST,
                                        reason=reason,
                                        subject=subject or "user")
                # Вернем ошибки
                return self.response
            else:
                user.set_password(self.password)
                user.save()

                expiry = str(datetime.date.today() + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_DAYS))
                payload = json.dumps({'id': user.userId, 'usrnm': user.username, 'exp': expiry})
                token = encrypt(payload, settings.SECRET_KEY)

                # Все удачно вернем данные
                self.response.data = {
                    "userId": user.userId,
                    "token": token
                }
                self.response.to_json()
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authentication")
        return self.response


    def action(self, data):
        userId = self.get_data('userId')
        password = self.get_data('password')
        username = self.get_data('username')
        # Можно добавить и другие поля

        if userId is None or password is None or username is None:
            return None

        token = self.get_token(user=userId)
        # hasBilling: boolean (Required)
        # Определяет, на чьей стороне производится биллинг по данному пользователю.
        #
        # true - в стороннем сервисе
        #
        # false - на стороне Эвотор

        if token is None:
            return None

        return {
            "userId": userId,
            "hasBilling": False,
            "token": token.key
        }


"""

{
    u'timestamp': 1504168645290, 
    u'version': 2, 
    u'type': u'ApplicationInstalled', 
    u'id': UUID('a99fbf70-6307-4acc-b61c-741ee9eef6c0'), 
    'data': 
        {
            u'timestamp': 1504168645290, 
            u'version': 2, 
            u'type': u'ApplicationInstalled', 
            u'id': u'a99fbf70-6307-4acc-b61c-741ee9eef6c0', 
            u'data': {
                        u'userId': u'01-000000000000001', 
                        u'productId': u'569af313-5fcf-43b4-9eb4-f81e8f17dac7'
                      }
        }
}
 
"""
