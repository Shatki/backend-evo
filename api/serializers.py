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

        class Meta:
            unique_together = ['productId', 'userId']
            # ordering = ['order']


class InstallationEventSerializer(serializers.ModelSerializer):
    data = InstallationSerializer(many=False)

    class Meta:
        model = InstallationEvent
        # depth = 2
        fields = ['id', 'timestamp', 'version', 'type', 'data']

    def create(self, getting_data):
        print '<v', getting_data, 'v>'
        installation_data = getting_data.pop('data')
        installation_event = InstallationEvent.objects.create(**getting_data)
        print '<', installation_event, '|||', installation_data, '>'
        for _data in installation_data:
            print '<!', _data, '!>'
            Installation.objects.create(installationId=installation_event.id, **_data)
        return installation_event


"""
{
  "id": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
  "timestamp": 11504168645290,
  "version": 2,
  "type": "ApplicationInstalled",
  "data": {
    "productId": "569af313-5fcf-43b4-9eb4-f81e8f17dac7",
    "userId": "01-000000000000001"
  }
}

"""