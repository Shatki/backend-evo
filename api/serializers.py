# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models import User
from rest_framework.authtoken.models import Token
from applications.models import Application, Subscription
from stores.models import Store
from products.models import Product
from applications.models import Application, InstallationEvent, Installation
from evotor.db import UserId


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'username', 'email', 'first_name', 'last_name']

    def to_representation(self, obj):
        return {
            'userId': str(obj.userId),
            'token': str(self.token)
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        self.token, self.created = Token.objects.get_or_create(user=user)
        return user


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
    # userId = serializers.CharField()

    class Meta:
        model = Installation
        fields = ['productId', 'userId']

        # class Meta:
        #    unique_together = ['productId', 'userId']
        #    # ordering = ['order']


class InstallationEventSerializer(serializers.ModelSerializer):
    data = InstallationSerializer(many=False, read_only=True)

    class Meta:
        model = InstallationEvent
        depth = 2
        fields = ['id', 'timestamp', 'version', 'type', 'data']

    def create(self, validated_data):
        try:
            """
                validated_data это комбинированные данные сериализатора и полученных данных
                которые хранятся под ключем 'data'. !!! У нас тоже в данных есть свой ключ 'data',
                поэтому первой строчкой выделяем полученные данные от данных сериализатора !!!
            """
            installation = validated_data.get('data', None)
            installation_data = installation.pop('data')
            # В данном случае productId относится к модели Application и приложение должно быть известно иначе ошибка
            installation_data_product = Application.objects.get(uuid=installation_data['productId'])

            # Тут мы ищем в базе пользователя Эвотор или создаем нового
            installation_data_user, created = User.objects.get_or_create(userId=installation_data['userId'])
            if created:
                # if the new user is created
                pass
            # Create a new event
            installation_event = InstallationEvent.objects.create(**installation)

            Installation.objects.create(installationId_id=installation_event.id,
                                        productId_id=installation_data_product.uuid,
                                        userId_id=installation_data_user.userId)
        except SyntaxError:
            return SyntaxError
            # print 'validated_data error:', validated_data['data']
        return installation_event
