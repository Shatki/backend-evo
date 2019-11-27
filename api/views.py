# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from api.response import APIView, status
from api.decorators import cloud_only, user_only
from api.models import Token

from applications.models import Application, Subscription, InstallationEvent, Installation
from stores.models import Store
from users.models import User
import requests


# Временная затычка
class DashboardView(APIView):
    # Todo: переделать главную страницу без Реакта
    template_name = "index.html"

    def get(self, request):
        self.data = self.get_params(request)
        validated_data = self.extract_data('token', 'user_id')
        if validated_data is None:
            self.response.add_error(error_code=status.ERROR_CODE_2003_REQUEST_ERROR,
                                    reason=_('GET request is wrong'),
                                    subject="Request")
            # Вернем ошибки
            return self.response
        context = {'token': validated_data['token'],
                   'user_id': validated_data['user_id']
                   }
        # print request.META
        return render_to_response(template_name=self.template_name, context=context)


class UserCreateView(APIView):
    """
        Регистрация учетной записи пользователя в нашем сервисе

        Создание нового пользователя и токена доступа
        Запрос:
        {
           "userId": "01-000000000000003",
           *"password": "password",
           *"username": "test3",
           "customField": "Дополнительные данные о пользователе"

        Ответ:
        {
           "token": "TLWHR7jA7HzBDmoRzUpHteNyDPqAkOAc/DP81JuM0dXpq8h60X+W0jh+PEWe1jkmJq/C6iW6YYafYzVGxhM3PABuDgTHX3QMeUcVUYRB9K39y7WKxISibx5FSm4Ek8Ek",
           "userId": "01-000000000000004"
        }
           *2-х дневный
        """

    @cloud_only
    def post(self, request, *args, **kwargs):
        # Получаем и преобразуем данные из request.body в JSON
        self.data = self.load_json(request)
        # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
        validated_data = self.extract_data('userId', 'password', 'username')
        if validated_data is None:
            self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                    reason=_('Fields error'),
                                    subject="Request")
            # Вернем ошибки
            return self.response
        # Создаем нового пользователя или получаем неактивную запись
        try:
            user, created = User.objects.get_or_create(userId=validated_data['userId'])
            user.username = validated_data['username']
            user.set_password(validated_data['password'])
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.response.add_error(status.ERROR_CODE_2005_USER_EXIST,
                                    reason=reason,
                                    subject=subject or "user")
            # Вернем ошибки
            return self.response
        else:
            # Обновление информации о пользователе
            if created:
                # Todo: Создан новый пользователь иначе пользователь обновлен
                pass
            user.save()
            # Все удачно вернем данные
            self.response.data = {
                "userId": user.userId,
                "token": self.create_token(user=user)
            }
            self.response.to_json()
        return self.response


class UserVerifyView(APIView):
    """
        Авторизация существующего пользователя в нашем сервисе с помощью данных учётной записи Личного кабинета Эвотор.

        Под пользователем понимается мастер-аккаунт владельца бизнеса в нашем сервисе.

        Запрос:
        {
            "userId": "01-000000000000004",
            "password": "password",
            "username": "test4"
        }

        Ответ:
        {
            "token": "S170jf2B3n2f7Yxk1kTsFDOaX1M8MdRzGnYSiMpYLRFPqTCc34DFpDGFz5DadPoM/ZF/qwC3SdapE8H/kCV3+p1pSZEZdOqStbMZregliYEMT7nyMbKriX0LJNM4pALS",
            "hasBilling": False,
            "userId": "01-000000000000004"
        }
    """

    @cloud_only
    def post(self, request, *args, **kwargs):
        # Получаем и преобразуем данные из request.body в JSON
        self.data = self.load_json(request)
        # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
        validated_data = self.extract_data('userId', 'password', 'username')
        if validated_data is None:
            self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                    reason=_('Fields error'),
                                    subject="Request")
            # Вернем ошибки
            return self.response
        # Получаем пользователя
        try:
            user = User.objects.get(userId=validated_data['userId'],
                                    username=validated_data['username'])
            if not user.check_password(validated_data['password']):
                raise ValueError(_("Password is incorrect"))
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.response.add_error(status.ERROR_CODE_1006_WRONG_DATA,
                                    reason=reason,
                                    subject=subject or "user")
            # Вернем ошибки
            return self.response
        else:
            # Все удачно вернем данные
            self.response.data = {
                "userId": validated_data['userId'],
                "hasBilling": False,
                "token": self.create_token(user=user)
            }
            self.response.to_json()
            # HTTP 200 OK
            return self.response


class UserTokenView(APIView):
    """
        Токен Облака Эвотор для авторизации запросов к Облаку Эвотор.

        Запрос:
        {
            "userId": "01-000000000000004",
            "token": "f46b89a5-8e80-4591-b1aa-94551790464b"
        }

        Ответ:
        HTTP 200 OK
    """

    @cloud_only
    def post(self, request, *args, **kwargs):
        # Получаем и преобразуем данные из request.body в JSON
        self.data = self.load_json(request)
        # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
        validated_data = self.extract_data('userId', 'token')
        if validated_data is None:
            self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                    reason=_('Fields error'),
                                    subject="Request")
            # Вернем ошибки
            return self.response
        # Запишем токен доступа
        try:
            user = User.objects.get(userId=validated_data['userId'])
            token, created = Token.objects.get_or_create(user=user)
            if created:
                # Todo: Для пользователя получен токен первый раз, что дальше?
                pass
            token.key = validated_data['token']
            token.save()
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.response.add_error(status.ERROR_CODE_2003_REQUEST_ERROR,
                                    reason=reason,
                                    subject=subject or "userId")
            # Вернем ошибки
            return self.response
        return self.response


class SubscriptionEventView(APIView):
    """
        Связанные с биллингом события, которые Облако Эвотор передаёт в наш сервис.

        Запрос:
        {
            "subscriptionId": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
            "productId": "c0d01x35-5193-4cc2-9bfb-be20e0679498",
            "userId": "01-000000000000001",
            "timestamp": "2017-04-20T18:26:37.753+0000",
            "sequenceNumber": 4,
            "type": "SubscriptionCreated",
            "planId": "example",
            "trialPeriodDuration": "P14DT",
            "deviceNumber": 35
        }

        {
            "subscriptionId":"e9f1a3ee-e78d-49b3-93d6-389f718ba8ec",
            "productId":"59fea9cb-0817-4431-9fb7-594f81584110",
            "userId":"01-000000000738894",
            "nextBillingDate":"2019-11-28T21:14:03.486Z",
            "sequenceNumber":4,
            "timestamp":"2019-10-28T21:14:12.174Z",
            "type":"SubscriptionRenewed"
            }

        Ответ:
        HTTP 200 OK
    """

    @cloud_only
    def post(self, request, *args, **kwargs):
        # Получаем и преобразуем данные из request.body в JSON
        self.data = self.load_json(request)
        # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
        validated_data = self.extract_data('subscriptionId',
                                       'productId',
                                       'userId',
                                       'timestamp',
                                       'sequenceNumber',
                                       'type',
                                       'planId',
                                       'trialPeriodDuration',
                                       'deviceNumber')
        if validated_data is None:
            self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                    reason=_('Fields error'),
                                    subject="Request")
            # Вернем ошибки
            return self.response
            # Запишем токен доступа
        try:
            user = User.objects.get(userId=validated_data['userId'])
            product, created = Application.objects.get_or_create(pk=validated_data['productId'])
            if created:
                # Todo: Создано новое приложение
                pass
            Subscription.objects.create(subscriptionId=validated_data['subscriptionId'],
                                        productId=product,
                                        userId=user,
                                        timestamp=validated_data['timestamp'],
                                        sequenceNumber=validated_data['sequenceNumber'],
                                        type=validated_data['type'],
                                        planId=validated_data['planId'],
                                        trialPeriodDuration=validated_data['trialPeriodDuration'],
                                        deviceNumber=validated_data['deviceNumber'])
        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.response.add_error(status.ERROR_CODE_2003_REQUEST_ERROR,
                                    reason=reason,
                                    subject=subject or "subscription")
            # Вернем ошибки
            return self.response
        # HTTP 200 Ok
        return self.response


class InstallationEventView(APIView):
    """
        Связанные с установкой и удалением приложения события, которые облако Эвотор передаёт в наш сервис.

        Запрос:
        {
            "id": "a99fbf70-6307-4acc-b61c-741ee9eef6c0",
            "timestamp": 1504168645290,
            "version": 2,
            "type": "ApplicationInstalled",
            "data": {
                    "productId": "string",
                    "userId": "01-000000000000001"
                    }
        }

        Ответ:
        HTTP 200 OK
    """

    @cloud_only
    def post(self, request, *args, **kwargs):
        self.data = self.load_json(request)
        # Всю работу с токенами делает миддлварь, мы только берем данные из запроса
        validated_data = self.extract_data('id',
                                       'timestamp',
                                       'version',
                                       'type',
                                       'data')

        try:
            # Сначала найдем пользователя
            user, created = User.objects.get_or_create(userId=validated_data['data']['userId'])
            if created:
                # Todo: Создали нового пользователя, без пароля
                print 'Перезаписано событие инсталляции c id: ', user.userId
                pass

            installationEvent, created = InstallationEvent.objects.get_or_create(
                id=validated_data['id'],
                timestamp=validated_data['timestamp']
            )
            # installationEvent.timestamp = validated_data['timestamp']
            installationEvent.version = validated_data['version']
            installationEvent.type = validated_data['type']
            installationEvent.save()
            if not created:
                # Todo: Инсталляция с таким  Id уже была, нужно разобраться
                print 'Перезаписано событие инсталляции c id: ', installationEvent.id
                pass

            product, created = Application.objects.get_or_create(uuid=validated_data['data']['productId'])
            if created:
                # Todo: Создано новое приложение, почему его не было в базе?
                print 'Создано новое приложение c uuid:', product.uuid
                pass

            installation, created = Installation.objects.get_or_create(
                productId=product,
                userId=user,
            )
            installation.installationId = installationEvent
            installation.save()

            if created:
                # Todo: Создана новая запись Installation
                pass

        except Exception as e:
            reason, subject = self.decode_exception(e)
            self.response.add_error(status.ERROR_CODE_2003_REQUEST_ERROR,
                                    reason=reason,
                                    subject=subject or "installation")
            # Вернем ошибки
            return self.response


class StoresListView(APIView):
    def get(self, request, token, *args, **kwargs):
        url = "https://api.evotor.ru/api/v1/inventories/stores/search"
        # data = {'data': [{'key1': 'val1'}, {'key2': 'val2'}]}
        headers = {
            'X-Authorization': token,
            'Content-Type': 'application/json'
        }
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            self.response.data = result.text
            self.response.to_json()
        else:
            self.response.add_error(error_code=result.status_code,
                                    reason=_('Request error'),
                                    subject="Stores")

        return self.response


class ProductsListView(APIView):
    """
        Запрос информации с облака Эвотор с обновлением БД
        Так же должна сверяться информация

    """
    @user_only
    def get(self, request, store_uuid, *args, **kwargs):
        # url = "https://api.evotor.ru/api/v1/inventories/stores/20180507-447F-40C1-8081-52D4B03CD7AB/products"
        data = [
                {
                    "uuid": "011845e5-d2f3-433e-a961-dcdbd4e6927b",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Адаптер DVI-D to HDMI Exegate 25M\/19F",
                    "code": "86",
                    "barCodes": [
                        "4897040852920"
                    ],
                    "price": 150,
                    "costPrice": 87,
                    "quantity": 3,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "2d852d4f-48c2-4db3-b27d-f9be610a3408",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Адаптер для установки SSD\/HDD 2.5\" в отсек DVD, 12.6mm",
                    "code": "116",
                    "barCodes": [],
                    "price": 400,
                    "costPrice": 250,
                    "quantity": 3,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "900e9658-02fc-4c40-be60-093683c72a15",
                    "group": False,
                    "hasVariants": None,
                    "type": "NORMAL",
                    "name": "SvetoCopy Бумага офисная А4 500л",
                    "code": "5",
                    "barCodes": [
                        "4605817132102",
                        "4605817132119"
                    ],
                    "price": 260,
                    "costPrice": 232,
                    "quantity": 43,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "1194fc78-50dd-4d93-a2cb-11f8b93418e9",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Антивирус Dr.Web Security Space 3 ПК 1 год",
                    "code": "101",
                    "barCodes": [
                        "4607141351297"
                    ],
                    "price": 1500,
                    "costPrice": 1150,
                    "quantity": 3,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "7442d67b-dd94-49f6-a2a4-8bbc0a63b15d",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Барабан Content для Samsung ML-1210\/1250\/4500\/Xerox 3110",
                    "code": "537",
                    "barCodes": [
                        "2000000000268"
                    ],
                    "price": 350,
                    "costPrice": 250,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "192416",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "8cc62770-fea1-4f5e-a2cc-f3eeaf727d97",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Барабан Content для HP 1005\/1006\/1505\/1102",
                    "code": "538",
                    "barCodes": [
                        "4690665027182",
                        "V0032548"
                    ],
                    "price": 200,
                    "costPrice": 85.52,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "90dd1bd3-947f-4668-8bb0-e43ecef87470",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Барабан Content для HP Color LJ Pro M252\/277\/452\/477\/M154A",
                    "code": "546",
                    "barCodes": [
                        "V0034046"
                    ],
                    "price": 300,
                    "costPrice": 147.36,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Компьютерные комплектующие",
                    "code": "604",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": None,
                    "articleNumber": None,
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "72856675-1826-48b8-bbe5-d7aa788e722f",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Материнские платы",
                    "code": "594",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "e8d08c80-2c51-4cc5-b25f-a2f993a0079f",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Корпуса",
                    "code": "600",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "e3a235a3-aeaf-4bdc-86dd-7cecb2395daf",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Видеокарты",
                    "code": "595",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "5aee69ad-1670-4fa5-a103-9a79171a7032",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Накопители",
                    "code": "598",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "a47216aa-f058-40ef-9725-9eea7fd99bc1",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Блоки питания",
                    "code": "599",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "822455cf-20a1-42ec-ad9d-4c548f1cc08f",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Процессоры",
                    "code": "593",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "3f14d222-afbc-4676-9b57-b79c1c52e82d",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Звуковые карты",
                    "code": "602",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "bc2c289d-d71b-4021-9df1-bdf11b0b0ca5",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Программное обеспечение",
                    "code": "606",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": None,
                    "description": None,
                    "articleNumber": None,
                    "parentUuid": None,
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "f8c2581b-d146-4885-9aee-681e4d3614b7",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Оперативная память",
                    "code": "596",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "0a4d7614-5480-4d7b-9ed2-705d8e03f8b6",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Системы охлаждения",
                    "code": "597",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "cc6215ca-b114-448e-96be-9568dca27301",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Приводы",
                    "code": "601",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "b881b484-85c3-4770-a158-4d0bc06cd417",
                    "group": True,
                    "hasVariants": False,
                    "type": None,
                    "name": "Кабели",
                    "code": "603",
                    "barCodes": None,
                    "price": None,
                    "costPrice": None,
                    "quantity": "0.000",
                    "measureName": "шт",
                    "tax": None,
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "eb76eb70-0576-4b7a-b0b0-bb6ede202e84",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "d2d438dd-897e-473f-ba00-011d4005aed6",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Процессор AMD soc-AM4 A8-9600 OEM 4\/4 Cores (3.1GHz,3.4GHz Max\/2Mb\/28nm) Radeon R7 int. 65W",
                    "code": "255",
                    "barCodes": [
                        "2000000000060"
                    ],
                    "price": 3590,
                    "costPrice": 2694,
                    "quantity": 2,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "822455cf-20a1-42ec-ad9d-4c548f1cc08f",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
                {
                    "uuid": "20eb13d6-c261-4cec-b18a-7ac32420a324",
                    "group": False,
                    "hasVariants": False,
                    "type": "NORMAL",
                    "name": "Процессор Intel soc-1151v2 Pentium G5400 OEM 2\/4 Cores (3.7GHz\/4Mb\/14nm\/DMI) UHD Graphics 610 int., 65W",
                    "code": "254",
                    "barCodes": [
                        "2000000000053"
                    ],
                    "price": 5800,
                    "costPrice": 5063,
                    "quantity": 0,
                    "measureName": "шт",
                    "tax": "NO_VAT",
                    "allowToSell": True,
                    "description": "",
                    "articleNumber": "",
                    "parentUuid": "822455cf-20a1-42ec-ad9d-4c548f1cc08f",
                    "alcoCodes": None,
                    "alcoholByVolume": None,
                    "alcoholProductKindCode": None,
                    "tareVolume": None
                },
            ]
        url = "https://api.evotor.ru/api/v1/inventories/stores/%s/products" % store_uuid
        headers = {
            'X-Authorization': request.META.get('HTTP_X_AUTH_TOKEN', b''),
            'Content-Type': 'application/json'
        }
        self.response.data = str(data)  # result.text
        self.response.to_json()
        """
        if result.status_code == status.HTTP_200_OK:
            # Todo обновление БД и сверка с данными Эвотора
            self.response.data = result.text
            self.response.to_json()
        else:
            self.response.add_error(error_code=result.status_code,
                                    reason=_('Request error'),
                                    subject="Stores")
        
        """
        # result = requests.get(url, headers=headers)

        return self.response
