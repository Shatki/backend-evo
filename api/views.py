# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from users.models import User
from api import serializers
from rest_framework import generics
from django.shortcuts import render


# Create your views here.
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
