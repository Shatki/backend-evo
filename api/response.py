# -*- coding: utf-8 -*-
import json
import status
import datetime
import evotor.settings as settings
from api.crypto import encrypt
from django.views.generic.base import View
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from api.models import Token


class APIResponse(HttpResponse):
    def __init__(self, data=b'', status_code=status.HTTP_200_OK,
                 error_code=None, reason=None, subject=None, **kwargs):
        self.data = data
        if self.data is not None:
            self.to_json()
        self.content = b''
        self.errors = []
        self.status_code = status_code
        if error_code:
            self.add_error(error_code=error_code, reason=reason, subject=subject)
        kwargs.setdefault('content_type', 'application/json')
        super(APIResponse, self).__init__(content=self.content, status=self.status_code, **kwargs)

    def to_json(self):
        self.content = json.dumps(self.data, cls=DjangoJSONEncoder)

    def __make_response__(self):
        """
        Создание ответа API
        Метод класса для формирования ответа из данных класса
        :return: None
        """
        if len(self.errors) > 0:
            # Если есть ошибки, то формируем ответ с информацией об ошибках
            self.data = {
                "errors": self.errors
            }
            self.status_code = self.status_code
        else:
            # Если ошибок нет, то отправляем нормальный ответ с требуемыми данными
            self.status_code = status.HTTP_200_OK

    def add_error(self, error_code, reason=None, subject=None):
        # Тут алгоритм присвоения статуса кода ответа
        try:
            self.status_code = status.errors[error_code]
        except KeyError as e:
            # Сервер ничего не ответил кроме кода ошибки
            reason = reason or e.args[0]
            subject = subject or "undefined error"
            # можно также присвоить значение по умолчанию вместо бросания исключения
            self.status_code = error_code or status.HTTP_400_BAD_REQUEST
        self.errors.append({
            "code": error_code,
            # Причина возникновения ошибки
            "reason": reason,
            # Название неизвестного или отсутствующего поля
            "subject": subject
        })
        self.__make_response__()
        self.to_json()


class APIView(View):
    """
        Представление API
        :return: self.response (объект HttpResponse)
    """

    def __init__(self):
        self.response = APIResponse()
        self.data = None
        super(APIView, self).__init__()

    @staticmethod
    def decode_exception(exception):
        e = exception.args[0].split(': ')
        return e[0] if e[0] is not None else "Unexpected", e[1] if len(e) > 1 else None

    def action(self, *args, **kwargs):
        pass

    def load_json(self, request):
        # POST only
        # Получаем и преобразуем данные из request.body в JSON
        try:
            return json.loads(request.body.decode(settings.CODING))
        except ValueError as e:
            # reason, subject = self.decode_exception(e)
            self.response.add_error(error_code=status.ERROR_CODE_2001_SYNTAX_ERROR,
                                    reason=_(e.args[0]),
                                    subject="json")
            # Вернем ошибки
            return self.response

    def get_params(self, request):
        try:
            return request.GET
        except ValueError as e:
            # reason, subject = self.decode_exception(e)
            self.response.add_error(error_code=status.ERROR_CODE_2001_SYNTAX_ERROR,
                                    reason=_(e.args[0]),
                                    subject="GET")

    def extract_data(self, *args):
        """
            Запрашивает поля с данными из self.data c валидацией на присутствие/отсутствие/Null поле

            :param args: Запрашиваемые поля
            :return: validated_data
            Todo: Валидацию полученных полей из запроса на соответствие с Regex
        """
        validated_data = {}
        for field in args:
            try:
                # Попытка получить поле из запроса
                field_data = self.data[field]
                # Валидация на непустое поле
                if field_data is None:
                    # JSON Поле есть, но оно пустое
                    self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                            reason="missing data",
                                            subject=field,
                                            )
            except Exception as e:
                # Совсем отсутствует JSON поле
                self.response.add_error(error_code=status.ERROR_CODE_2002_FIELDS_ERROR,
                                        reason="missing field",
                                        subject=e.args[0],
                                        )
            else:
                validated_data.update({
                    field: field_data
                })

        return validated_data if len(validated_data) == len(args) else None

    def get_token(self, user):
        """
            Получение токена пользователя для авторизации запросов к Облаку
            :param user: пользователь
            :return: токен пользователя для авторизации запросов к Облаку
        """
        try:
            return Token.objects.get(user=user)
        except Exception as e:
            reason, subject = self.decode_exception(e)
            # эту ошибку нужно записать в логи
            self.response.add_error(status.ERROR_CODE_3000_DB_ERROR,
                                    reason=reason,
                                    subject=subject or "db")
            return None

    def create_token(self, user):
        """
            Создание токена пользователя для авторизации запросов из Облака
            :param user: пользователь
            :return: токен пользователя для авторизации запросов из Облака
        """
        if user is None:
            raise ValueError(_('User cannot be Null'))
        expiry = str(datetime.date.today() + datetime.timedelta(days=settings.AUTH_TOKEN_EXPIRY_DAYS))
        payload = json.dumps({'id': user.userId, 'usrnm': user.username, 'exp': expiry})
        return encrypt(payload, settings.SECRET_KEY)
