# -*- coding: utf-8 -*-
import django.db.models as models
from django.core.exceptions import ValidationError
import re

DEFAULT_USERID = u'01-0000000000000001'


class UserIdField(models.BigIntegerField):
    """
        ID field uses in evotor users' model
    """
    DEFAULT_MASK = '00-000000000000000'
    PATTERN_USERID = r'[0-9]{2}-[0-9]{15}'
    SEPARATOR_CONST = '-'
    description = "Evotor UserId model object"

    def __init__(self, *args, **kwargs):
        kwargs['null'] = False
        super(UserIdField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        print 'deconstruct'
        name, path, args, kwargs = super(UserIdField, self).deconstruct()
        # del kwargs["max_length"], kwargs["null"]
        return name, path, args, kwargs

    # def db_type(self, connection):
    #     return 'userId'

    def get_internal_type(self):
        print 'get_internal_type'
        return 'UserIdField'

    def to_python(self, val):
        """
            Convert the input database BigIntenger value into python string, raises
            django.core.exceptions.ValidationError if the data can't be converted.
        """
        print 'to_python: ', val, type(val)
        # Преобразует значение из базы данных (или сериалайзера) в объект Python.
        # Метод обратный get_prep_value() - подготавливает значение для поля для вставки в базу данных.
        #
        # По умолчанию возвращает value, что обычно подходит, если бэкенд уже возвращает правильный объект Python.

        if isinstance(val, int):
            user_id = ((self.DEFAULT_MASK + str(val))[-17:])
            return u'{}-{}'.format(user_id[0:2], user_id[2:18])
        # Если что-то иное
        else:
            raise ValidationError(u'Unknown DB data format value')

    def get_prep_value(self, val, *args, **kwargs):
        """
            Convert value to db UserId BigInteger before save
        """
        # Преобразует val в значение для бэкенда базы данных. По умолчанию возвращает value,
        # если prepared=True, иначе – результат get_prep_value()
        print 'get_prep_value: ', val
        if val is None:
            raise ValidationError(u'The value cannot to be is None')
        if re.match(self.PATTERN_USERID, val) and len(val) == 18:
            # Возвращаем значения в базу
            return val.replace('-', "").lstrip('0')
        raise ValidationError(u'Bad value')

    def value_to_string(self, obj):
        # Преобразование значения поля для сериалайзера
        print 'value_to_string: ', obj, self._get_val_from_obj(obj)
        # obj: 01-000000000738894 <class 'users.models.User'>
        val = self._get_val_from_obj(obj)
        # val: 01-000000000738894 <type 'unicode'>
        # Преобразование в читаемую форму
        return val

    def from_db_value(self, val, *args, **kwargs):
        print 'from_db_value: ', val, self.to_python(val)
        # Преобразование значений базы данных в объекты Python
        return self.to_python(val)


