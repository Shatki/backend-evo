# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404

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
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        queryset = User.objects.all()
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk):
        user = self.get_object(pk)
        serializer = serializers.StoreSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk):
        pass


@permission_classes((permissions.AllowAny,))
class StoreViewSet(viewsets.ViewSet):
    """
        Просмотр всех магазинов или создание новых, а также редактирование существующих
    """
    @staticmethod
    def get_object(pk):
        try:
            return Store.objects.get(pk=pk)
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

    def retrieve(self, request, pk):
        store = self.get_object(pk)
        serializer = serializers.StoreSerializer(store)
        return Response(serializer.data)

    def update(self, request, pk):
        store = self.get_object(pk)
        serializer = serializers.StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk):
        store = self.get_object(pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)