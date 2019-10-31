# -*- coding: utf-8 -*-
from datetime import datetime
import json
import evotor.settings as settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext_lazy as _
from api import status
from api.crypto import decrypt
from users.models import User
from api.models import Log
from api.response import APIResponse


class LogsMiddleware(MiddlewareMixin):
    """
        Миддлварь для логирования HTTP запросов
    """
    log = None
    content = None

    def process_request(self, request):
        # Фильтруем только запросы к API
        print request.META
        if request.META['PATH_INFO'][0:8] == u'/api/v1/':
            try:
                if request.method == "POST" or request.method == "OPTIONS":
                    self.content = str(request.body.decode('utf-8')).replace(',"', ', "')
                elif request.method == "GET":
                    self.content = str(request.GET)

                if self.content is not None:
                    self.log = Log.objects.create(request=self.content)
                    self.log.headers = str(request.META)    # .replace(',"', ', "')
                    self.log.save()

            except Exception as e:
                print 'process_request_exception: ', e.args[0]

    def process_response(self, request, response):
        if self.log is not None:
            try:
                self.log.response = response.content.decode(settings.CODING)
                self.log.status = response.status_code
                self.log.save()
            except Exception as e:
                print 'process_response_exceprion: ', e.args[0]
        return response


class HttpManagementMiddleware(MiddlewareMixin):
    """
        Миддлварь для управления HTTP запросами

        1. Переносит параметры GET запроса в заголовки
        2.
        3.
    """
    def process_request(self, request):
        # Переносим параметры GET запроса в заголовок
        if request.method == 'GET':
            try:
                if 'token' in request.GET:
                    request.META['HTTP_AUTH_TOKEN'] = request.GET['token']
                if 'user_id' in request.GET:
                    request.META['HTTP_AUTH_USER_ID'] = request.GET['user_id']
            except Exception as e:
                print 'HttpManagementMiddleware warning: ', e.args[0]


class TokenMiddleware(MiddlewareMixin):
    """
        Миддлварь, которая авторизует пользователя по токену в заголовке 'HTTP_AUTHORIZATION'

        1. Перехватывает заголовок
        2. Если в заголовке в HTTP_AUTHORIZATION есть токен, выделяем его
        3. Если токен Облака Эвотор, то не авторизуем пользователя и доступны:
            -   авторизация пользователя,
            -   создание пользователя,
            -   передача токена пользователя
        4. Если токен пользователя, то авторизуем его через токен

    """

    def process_request(self, request):
        # Если в заголовке нет авторизации -> пропускаем на сайт без авторизации
        request.META['HTTP_AUTH'] = settings.HTTP_AUTH_ANONYMOUS
        if 'HTTP_AUTHORIZATION' not in request.META:
            return None

        auth_header = request.META.get('HTTP_AUTHORIZATION', b'')
        if auth_header:
            auth = auth_header.split(" ")

            # If they specified an invalid token, let them know.
            # Проверяем заголовок - должен быть Authorization: Bearer evotor_token
            if len(auth) != 2 or auth[0].lower() != settings.AUTH_TOKEN_TYPE:
                return APIResponse(error_code=status.ERROR_CODE_1001_WRONG_TOKEN,
                                   reason=_('Improperly formatted token.'),
                                   subject="Authorization")
            try:
                token = auth[1].decode(settings.CODING)
            except UnicodeError:
                return APIResponse(error_code=status.ERROR_CODE_1001_WRONG_TOKEN,
                                   reason=_(
                                       'Invalid token header. Token string should not contain invalid characters.'),
                                   subject="Authorization")

            # Если в заголовке есть токен Облака Эвотор, то пропускаем
            if token == settings.AUTH_TOKEN_EVOTOR:
                # Пришел токен Облака Эвотор
                request.META['HTTP_AUTH'] = settings.HTTP_AUTH_CLOUD
            else:
                # Вдруг пришел плохой токен?
                if len(token) != 128:
                    return APIResponse(error_code=status.ERROR_CODE_1002_WRONG_USER_TOKEN,
                                       reason="Wrong user token",
                                       subject="Token")
                try:
                    req = decrypt(token, settings.SECRET_KEY)
                    decoded_dict = json.loads(req)
                except Exception as e:
                    return APIResponse(error_code=status.ERROR_CODE_1002_WRONG_USER_TOKEN,
                                       reason=e.args[0],
                                       subject="Token")
                userId = decoded_dict['id']
                username = decoded_dict['usrnm']
                expiry = decoded_dict['exp']

                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return APIResponse(error_code=status.ERROR_CODE_1002_WRONG_USER_TOKEN,
                                       reason=_('Invalid user token.'),
                                       subject="Token")

                if not user.is_active:
                    return APIResponse(error_code=status.ERROR_CODE_1006_WRONG_DATA,
                                       reason=_('User inactive or deleted.'),
                                       subject="User")

                if datetime.strptime(expiry, '%Y-%m-%d') < datetime.today():
                    return APIResponse(error_code=status.ERROR_CODE_1003_USER_TOKEN_EXPIRED,
                                       reason=_('Token Expired.'),
                                       subject="Token")

                # user = auth.authenticate(token=auth_header[1])
                request.user = user
                request.META['HTTP_AUTH'] = settings.HTTP_AUTH_USER
            return None
        else:
            return APIResponse(error_code=status.ERROR_CODE_2003_REQUEST_ERROR,
                               reason=_('Wrong Authorization data.'),
                               subject="Authorization")
