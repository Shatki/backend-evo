# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models import User
from applications.models import Subscription
from stores.models import Store
from products.models import Product
from applications.models import Application, Installation, InstallationData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'email', 'username', 'first_name', 'last_name', ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['uuid', 'address', 'name', 'code']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'name', 'group', 'parentUuid', 'type', 'quantity',
                  'measureName', 'tax', 'price', 'allowToSell', 'costPrice', 'description',
                  'articleNumber', 'code', 'barCodes', ]


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['name', 'uuid', 'version', ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscriptionId', 'productId', 'userId',
                  'timestamp', 'sequenceNumber', 'type',
                  'planId', 'trialPeriodDuration', 'deviceNumber', ]


class InstallationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installation
        fields = ['id', 'timestamp', 'version', 'type', 'data', ]


class InstallationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallationData
        fields = ['productId', 'userId', ]


