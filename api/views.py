# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404

from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api import serializers
from rest_framework import generics, permissions
from users.models import User
from stores.models import Store


# Create your views here.
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@permission_classes((permissions.AllowAny,))
class StoreList(APIView):
    """
        Просмотр всех магазинов или создание нового
    """
    def get(self, request, format=None):
        stores = Store.objects.all()
        serializer = serializers.StoreSerializer(stores, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.StoreSerializer(data=request.store)
        store = request.data.get('article')
        # Create an article from the above data

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"success": "Store '{}' created successfully".format(store_saved.name)})


@permission_classes((permissions.AllowAny,))
class StoreDetail(APIView):
    """
        Извлечение, обновление или удаление магазина
    """
    @staticmethod
    def get_object(uuid):
        try:
            return Store.objects.get(uuid=uuid)
        except Store.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        store = self.get_object(uuid)
        serializer = serializers.StoreSerializer(store)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        store = self.get_object(uuid)
        serializer = serializers.StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        store = self.get_object(uuid)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)