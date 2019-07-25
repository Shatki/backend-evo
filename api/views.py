# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404

from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.settings import api_settings

from api import serializers
from users.models import User
from applications.models import Subscription
from stores.models import Store


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
# Create your views here.
class UserViewSet(viewsets.ViewSet):
    """
            Просмотр пользователей
    """
    lookup_field = 'userId'
    lookup_value_regex = '[0-9]{2}-[0-9]{15}'

    @staticmethod
    def get_object(userId):
        try:
            return User.objects.get(userId=userId)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        queryset = User.objects.all()
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, userId):
        user = self.get_object(userId)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, userId):
        pass

    def partial_update(self, request, userId=None):
        pass

    def destroy(self, request, userId):
        pass


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
# Create your views here.
class SubscriptionViewSet(viewsets.ViewSet):
    """
            Просмотр пользователей
    """
    lookup_field = 'subscriptionId'
    lookup_value_regex = '[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(subscriptionId):
        try:
            return Subscription.objects.get(subscriptionId=subscriptionId)
        except Subscription.DoesNotExist:
            raise Http404

    def list(self, request):
        queryset = Subscription.objects.all()
        serializer = serializers.SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, subscriptionId):
        subscription = self.get_object(subscriptionId)
        serializer = serializers.SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def update(self, request, subscriptionId):
        pass

    def partial_update(self, request, subscriptionId=None):
        pass

    def destroy(self, request, subscriptionId):
        pass


@permission_classes((permissions.AllowAny,))
# Create your views here.
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