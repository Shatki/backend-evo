# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import get_object_or_404
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.settings import api_settings

from api import serializers
from users.models import User
from rest_framework.authtoken.models import Token
from applications.models import Subscription, InstallationEvent, Installation
from stores.models import Store


class UserCreateView(APIView):
    """
            Регистрация пользователя:

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
    # lookup_field = 'userId'
    # lookup_value_regex = '[0-9]{2}-[0-9]{15}'

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        # print "verify", userId
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if 'userId' in serializer.errors.keys() or 'username' in serializer.errors.keys():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class UserVerifyView(APIView):
    """
            Авторизация пользователя:
            Запрос:
            >{
                "userId": "01-000000000000001",
                "username": "И.Иванов",
                "password": "superpassword",
                "customField": "Дополнительные данные о пользователе"
            }

            Ответ:
            >{
                "userId": "01-000000000000001",
                "hasBilling": true,
                "token": "toaWaep4chou7ahkoogiu9Iusaht9ima"
            }
    """
    # lookup_field = 'userId'
    # lookup_value_regex = '[0-9]{2}-[0-9]{15}'

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    @staticmethod
    def get_object(userId):
        try:
            return User.objects.get(userId=userId)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        queryset = User.objects.all()
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Ищем пользователя или создаем об это запись в базе
        serializer = serializers.UserSerializer(data=request.data)
        userId = request.data.get('userId')
        print userId
        # Create a store from the above data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        userId = request.data.get('userId')
        print "verify", userId
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=userId)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # The request user is set as author automatically.
        serializer.save(data=self.request.data)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class SubscriptionViewSet(viewsets.ViewSet):
    """
            Просмотр пользователей
    """
    lookup_field = 'subscriptionId'
    lookup_value_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        queryset = Subscription.objects.all()
        serializer = serializers.SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class SubscriptionEventViewSet(viewsets.ViewSet):
    """
            События подписки

            Связанные с биллингом события, которые Облако Эвотор передаёт в сторонний сервис.

            Облако выполняет попытки передать события в течение двух суток, до тех пор пока не будет получен ответ
                    об успешной доставке события (200 ОК).

    """

    def create(self, request, *args, **kwargs):
        # Ищем пользователя по userId
        try:
            user = User.objects.get(userId=request.data.get('userId'))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,)
        subscription = request.data

        subscription['userId'] = user.id

        serializer = serializers.SubscriptionSerializer(data=subscription)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class StoreViewSet(viewsets.ViewSet):
    """
        Просмотр всех магазинов или создание новых, а также редактирование существующих
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'

    @staticmethod
    def get_object(uuid):
        try:
            return Store.objects.get(uuid=uuid)
        except Store.DoesNotExist:
            raise Http404

    def list(self, request):
        stores = Store.objects.all()
        serializer = serializers.StoreSerializer(stores, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = serializers.StoreSerializer(data=request.store)
        store = request.data.get('store')
        # Create a store from the above data

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"success": "Store '{}' created successfully".format(store_saved.name)})

    def retrieve(self, request, uuid):
        _uuid = uuid.lower().replace('-', '')
        store = self.get_object(uuid=_uuid)
        serializer = serializers.StoreSerializer(store)
        return Response(serializer.data)

    def update(self, request, uuid):
        store = self.get_object(uuid)
        serializer = serializers.StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, uuid=None):
        pass

    def destroy(self, request, uuid):
        store = self.get_object(uuid)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes((permissions.AllowAny,))
class InstallationViewSet(viewsets.ViewSet):
    """
           Журнал событий установки и удаления приложений
    """
    def list(self, request):
        installation_events = InstallationEvent.objects.all()
        serializer = serializers.InstallationEventSerializer(installation_events, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
# Create your views here.
class InstallationEventViewSet(viewsets.ViewSet):
    """
           События установки и удаления приложений
           Связанные с установкой и удалением приложения события, которые облако Эвотор передаёт в сторонний сервис
    """
    # parser_classes = (JSONParser,)
    # permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        # Ищем установленное приложение или создаем об это запись в базе
        # installation_data = installation_event.get('data')
        # print installation_data
        serializer = serializers.InstallationEventSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # The request user is set as author automatically.
        serializer.save(data=self.request.data)


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

