# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json
import evotor.settings as settings

from django.utils.translation import ugettext_lazy as _
from .response import APIView, status
from users.models import User
from api.models import Token
from applications.models import Application, Subscription, InstallationEvent, Installation
from stores.models import Store


class UserCreateView(APIView):
    """
        Регистрация учетной записи пользователя в нашем сервисе

        Создание нового пользователя и токена доступа
        Запрос:
        {
           "userId": "01-000000000000003",
           *"password": "password",
           *"username": "test3",
           "customField": "Дополнительные данные о пользователе"

        Ответ:
        {
           "token": "TLWHR7jA7HzBDmoRzUpHteNyDPqAkOAc/DP81JuM0dXpq8h60X+W0jh+PEWe1jkmJq/C6iW6YYafYzVGxhM3PABuDgTHX3QMeUcVUYRB9K39y7WKxISibx5FSm4Ek8Ek",
           "userId": "01-000000000000004"
        }
           *2-х дневный
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
            validated_data = self.get_data('userId', 'password', 'username')

            if validated_data is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Fields error'),
                                        subject="Request")
                # Вернем ошибки
                return self.response

            # Создаем нового пользователя
            try:
                user = User.objects.create(userId=validated_data['userId'],
                                           username=validated_data['username'])
            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_2005_USER_EXIST,
                                        reason=reason,
                                        subject=subject or "user")
                # Вернем ошибки
                return self.response
            else:
                user.set_password(validated_data['password'])
                user.save()

                # Все удачно вернем данные
                self.response.data = {
                    "userId": user.userId,
                    "token": self.create_token(user=user)
                }
                self.response.to_json()
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authentication")
        return self.response


class UserVerifyView(APIView):
    """
        Авторизация существующего пользователя в нашем сервисе с помощью данных учётной записи Личного кабинета Эвотор.

        Под пользователем понимается мастер-аккаунт владельца бизнеса в нашем сервисе.

        Запрос:
        {
            "userId": "01-000000000000004",
            "password": "password",
            "username": "test4"
        }

        Ответ:
        {
            "token": "S170jf2B3n2f7Yxk1kTsFDOaX1M8MdRzGnYSiMpYLRFPqTCc34DFpDGFz5DadPoM/ZF/qwC3SdapE8H/kCV3+p1pSZEZdOqStbMZregliYEMT7nyMbKriX0LJNM4pALS",
            "hasBilling": false,
            "userId": "01-000000000000004"
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
            validated_data = self.get_data('userId', 'password', 'username')
            if validated_data is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Fields error'),
                                        subject="Request")
                # Вернем ошибки
                return self.response

            # Получаем пользователя
            try:
                user = User.objects.get(userId=validated_data['userId'],
                                        username=validated_data['username'])
                if not user.check_password(validated_data['password']):
                    raise ValueError(_("Password is incorrect"))

            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_1006_WRONG_DATA,
                                        reason=reason,
                                        subject=subject or "user")
                # Вернем ошибки
                return self.response
            else:
                # Все удачно вернем данные
                self.response.data = {
                    "userId": validated_data['userId'],
                    "hasBilling": False,
                    "token": self.create_token(user=user)
                }
                self.response.to_json()
        else:
            self.response.add_error(status.ERROR_CODE_1001_WRONG_TOKEN,
                                    reason=_('Cloud token error'),
                                    subject="Authentication")
        return self.response


class UserTokenView(APIView):
    """
        Токен Облака Эвотор для авторизации запросов к Облаку Эвотор.

        Запрос:
        {
            "userId": "01-000000000000004",
            "token": "f46b89a5-8e80-4591-b1aa-94551790464b"
        }

        Ответ:
        HTTP 200 OK
    """

    def post(self, request, *args, **kwargs):
        # Авторизуем запрос только с облака
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
            validated_data = self.get_data('userId', 'token')

            if validated_data is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Fields error'),
                                        subject="Request")
                # Вернем ошибки
                return self.response

            # Запишем токен доступа
            try:
                user = User.objects.get(userId=validated_data['userId'])
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    # Todo: Для пользователя получен токен первый раз, что дальше?
                    pass
                token.key = validated_data['token']
                token.save()

            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_2003_REQUEST_ERROR,
                                        reason=reason,
                                        subject=subject or "userId")
                # Вернем ошибки
                return self.response

            return self.response


class SubscriptionEventView(APIView):
    """
        Связанные с биллингом события, которые Облако Эвотор передаёт в наш сервис.

        Запрос:
        {
            "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
            "productId": "c0d01x35-5193-4cc2-9bfb-be20e0679498",
            "userId": "01-000000000000001",
            "timestamp": "2017-04-20T18:26:37.753+0000",
            "sequenceNumber": 4,
            "type": "SubscriptionCreated",
            "planId": "example",
            "trialPeriodDuration": "P14DT",
            "deviceNumber": 35
        }

        Ответ:
        HTTP 200 OK
    """

    def post(self, request, *args, **kwargs):
        # Авторизуем запрос только с облака
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
            validated_data = self.get_data('subscriptionId',
                                           'productId',
                                           'userId',
                                           'timestamp',
                                           'sequenceNumber',
                                           'type',
                                           'planId',
                                           'trialPeriodDuration',
                                           'deviceNumber')

            if validated_data is None:
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason=_('Fields error'),
                                        subject="Request")
                # Вернем ошибки
                return self.response

                # Запишем токен доступа
            try:
                user = User.objects.get(userId=validated_data['userId'])
                product, created = Application.objects.get_or_create(pk=validated_data['productId'])
                if created:
                    # Todo: Создано новое приложение
                    pass
                Subscription.objects.create(subscriptionId=validated_data['subscriptionId'],
                                            productId=product,
                                            userId=user,
                                            timestamp=validated_data['timestamp'],
                                            sequenceNumber=validated_data['sequenceNumber'],
                                            type=validated_data['type'],
                                            planId=validated_data['planId'],
                                            trialPeriodDuration=validated_data['trialPeriodDuration'],
                                            deviceNumber=validated_data['deviceNumber'])
            except Exception as e:
                reason, subject = self.decode_exception(e)
                self.response.add_error(status.ERROR_CODE_2003_REQUEST_ERROR,
                                        reason=reason,
                                        subject=subject or "subscription")
                # Вернем ошибки
                return self.response

            return self.response
