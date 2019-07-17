# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from rest_framework import generics, permissions
from users.models import User
from stores.models import Store


# Create your views here.
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


@permission_classes((permissions.AllowAny,))
class StoreView(APIView):
    def get(self, request):
        stores = Store.objects.all()
        serializer = serializers.StoreSerializer(stores, many=True)
        return Response({"stores": serializer.data})

    def post(self, request):
        store = request.data.get('article')
        # Create an article from the above data
        serializer = serializers.StoreSerializer(data=store)
        if serializer.is_valid(raise_exception=True):
            store_saved = serializer.save()
        return Response({"success": "Store '{}' created successfully".format(store_saved.name)})
