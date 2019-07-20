# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
import uuid as pyUUID

from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets

from api import serializers
from rest_framework import generics, permissions
from users.models import User
from stores.models import Store


@permission_classes((permissions.AllowAny,))
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


@permission_classes((permissions.AllowAny,))
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