# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models import User
from applications.models import Subscription
from stores.models import Store
from products.models import Product
from applications.models import Application, InstallationEvent, Installation


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
        fields = ['productId', 'userId', ]


class InstallationEventSerializer(serializers.ModelSerializer):
    data = InstallationSerializer()

    class Meta:
        model = InstallationEvent
        fields = ['id', 'timestamp', 'version', 'type', 'data', ]

    def create(self, validated_data):
        data = validated_data.pop('data')
        installation = Installation.objects.create(**validated_data)
        for element in data:
            Installation.objects.create(installation=installation, **element)
        return installation


"""
{
  "id": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
  "timestamp": 15651571200000,
  "version": 2,
  "type": "ApplicationInstalled",
  "data": {
    "productId": "569af313-5fcf-43b4-9eb4-f81e8f17dac7",
    "userId": "01-000000000000001"
  }
}

"""