# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from evotor.settings import EVOTOR_TOKEN
from datetime import datetime
import json
from django.db.utils import IntegrityError

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .response import APIResponse, status
from users.models import User, Token
from applications.models import Subscription, InstallationEvent, Installation
from stores.models import Store


class UserCreateView(APIResponse):
    """
        Регистрация учетной записи пользователя:
            Запрос:
            >{
                "userId": "01-000000000000003",
                "password": "crjhgbjy303",
                "username": "test3",
                "customField": "Дополнительные данные о пользователе"
            }
            Ответ:
            >{
                "userId": "01-000000000000003",
                "token": "toaWaep4chou7ahkoogiu9Iusaht9ima"
            }
        """
    def action(self, data):
        userId = self.get_data('userId')
        password = self.get_data('password')
        username = self.get_data('username')

        if userId is None or password is None or username is None:
            return None

        try:
            user = User.objects.create(userId=userId, username=username)
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.add_error(status.ERROR_CODE_2005_USER_EXIST,
                           reason=reason,
                           subject=subject or "user")
            return None
        else:
            user.set_password(password)
            user.save()

        token = self.create_token(user=user)
        # hasBilling: boolean (Required)
        # Определяет, на чьей стороне производится биллинг по данному пользователю.
        #
        # true - в стороннем сервисе
        #
        # false - на стороне Эвотор

        # Все удачно, - возвращаем ответ 200
        return {
                "userId": userId,
                "hasBilling": False,
                "token": token.key
            }


class UserCreateVerify(APIResponse):
    """
    Авторизация пользователя:
        Запрос:
        >{
            "userId": "01-000000000000003",
            "password": "crjhgbjy303",
            "username": "test3"
        }
        Ответ:
        >{
            "userId": "01-000000000000003",
            "token": "toaWaep4chou7ahkoogiu9Iusaht9ima"
        }
    """
    def action(self, data):
        userId = self.get_data('userId')
        password = self.get_data('password')
        username = self.get_data('username')
        # Можно добавить и другие поля

        if userId is None or password is None or username is None:
            return None

        token = self.get_token(user=userId)

        if token is None:
            return None

        return {
                "userId": userId,
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

