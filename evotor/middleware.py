# -*- coding: utf-8 -*-
import datetime

from django.utils.deprecation import MiddlewareMixin

from api import status
from jose import jwt, JWTError

from evotor import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext_lazy as _
from users.models import User
from api.response import APIResponse

from .exeptions import TokenVerificationException


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
        auth_header = request.META.get('HTTP_AUTHORIZATION', b'').split()

        # Проверяем заголовок - должен быть Authorization: Bearer evotor_token
        if not auth_header or auth_header[0].lower() != settings.AUTH_TOKEN_TYPE:
            return None

        # If they specified an invalid token, let them know.
        if len(auth_header) != 2:
            return HttpResponseBadRequest("Improperly formatted token")

        try:
            token = auth_header[1].decode("utf-8")
        except UnicodeError:
            return APIResponse(code=status.ERROR_CODE_2003_REQUEST_ERROR,
                               reason=_('Invalid token header. Token string should not contain invalid characters.'),
                               subject="Authorization")

        if token != settings.AUTH_TOKEN_EVOTOR:

            # Вдруг пришел плохой токен?
            try:
                decoded_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except JWTError as e:
                return APIResponse(code=status.ERROR_CODE_1002_WRONG_USER_TOKEN,
                                   reason=e.args[0],
                                   subject="Token")

            username = decoded_dict.get('username', None)
            expiry = decoded_dict.get('expiry', None)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return APIResponse(code=status.ERROR_CODE_1002_WRONG_USER_TOKEN,
                                   reason=_('Invalid token.'),
                                   subject="Token")

            if not user.is_active:
                return APIResponse(code=status.ERROR_CODE_1006_WRONG_DATA,
                                   reason=_('User inactive or deleted.'),
                                   subject="User")

            if expiry < datetime.date.today():
                return APIResponse(code=status.ERROR_CODE_1003_USER_TOKEN_EXPIRED,
                                   reason=_('Token Expired.'),
                                   subject="Token")

            # user = auth.authenticate(token=auth_header[1])
            request.user = user
        else:
            # Пришел токен Облака Эвотор
            pass
