# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from evotor.settings import EVOTOR_TOKEN
from datetime import datetime
import json

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import status
from .response import APIResponse
from users.models import User, Token
from applications.models import Subscription, InstallationEvent, Installation
from stores.models import Store


class UserCreateView(APIResponse):
    def action(self, data):
        userId = data['userId']
        token = Token.objects.get(user=userId)
        return {
                "userId": userId,
                "hasBilling": False,
                "token": token.key
            }, status.HTTP_200_OK


def user_verify(request):
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
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        userId = data['userId']
        token = Token.objects.get(user=userId)
        return APIResponse.response(status.HTTP_200_OK)
    else:
        APIResponse.response(status.HTTP_400_BAD_REQUEST)


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

