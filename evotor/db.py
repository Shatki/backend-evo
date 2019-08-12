# -*- coding: utf-8 -*-
import django.db.models as models
from django.utils.six import with_metaclass
from django.core.exceptions import ValidationError

DEFAULT_USERID = '01-0000000000000001'


class UserIdField(with_metaclass(models.BigIntegerField, models.Field)):
    """
        ID field uses in evotor users' model
    """
    DEFAULT_MASK = '00-000000000000000'
    SEPARATOR_CONST = '-'
    description = "Evotor UserId model object"

    __metaclass__ = models.SubfieldBase

    @staticmethod
    def _is_string(val):
        try:
            return isinstance(val, unicode)
        except NameError:
            return isinstance(val, str)

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        kwargs['blank'] = False
        kwargs['null'] = False
        super(UserIdField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UserIdField, self).deconstruct()
        del kwargs["max_length"], kwargs["blank"], kwargs["null"]
        return name, path, args, kwargs

    # def db_type(self, connection):
    #     return 'userId'

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def to_python(self, val):
        """
            Convert the input database BigIntenger value into python string, raises
            django.core.exceptions.ValidationError if the data can't be converted.
        """

        # Преобразует значение из базы данных (или сериалайзера) в объект Python.
        # Метод обратный get_prep_value() - подготавливает значение для поля для вставки в базу данных.
        #
        # По умолчанию возвращает value, что обычно подходит, если бэкенд уже возвращает правильный объект Python.

        # Если строка
        if self._is_string(val):
            user_id = ((self.DEFAULT_MASK + str(val))[-17:])
            return u'{}-{}'.format(user_id[0:2], user_id[2:18])
        # Если что-то иное
        else:
            raise ValidationError(u'Unknown DB data format')

    def get_db_prep_value(self, val, *args, **kwargs):
        """
            Convert value to db UserId BigInteger before save
        """
        # Преобразование значений запроса в значения базы данных
        if val is None:
            raise ValidationError(u'The value cannot to be is None')
        if len(val) == 18 and val[2] == '-':
            # Возвращаем значения в базу
            return val.replace('-', "").lstrip('0')
        raise ValidationError(u'Bad value')

    def value_to_string(self, obj):
        # Преобразование значения поля для сериалайзера
        val = self._get_val_from_obj(obj)
        # Преобразование в читаемую форму
        return self.to_python(val)

    def from_db_value(self, val, *args, **kwargs):
        # Преобразование значений базы данных в объекты Python
        return self.to_python(val)


