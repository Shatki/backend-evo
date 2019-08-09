# -*- coding: utf-8 -*-
import django.db.models as models


class UserIdField(models.BigIntegerField):
    # TODO(Shatki):
    # * should we take care of transforming between time zones in any way here ?
    # * get default datetime format from settings ?
    DEFAULT_MASK = '00-000000000000000'
    SEPARATOR_CONST = '-'
    # TODO(Shatki):
    # * metaclass below just for Django < 1.9, fix a if stmt for it?
    # __metaclass__ = models.SubfieldBase
    description = "Evotor UserId model object"

    @staticmethod
    def _is_string(val):
        try:
            return isinstance(val, unicode)
        except NameError:
            return isinstance(val, str)

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def to_python(self, val):
        # Преобразует значение из базы данных (или сериалайзера) в объект Python.
        # Метод обратный get_prep_value().
        #
        # По умолчанию возвращает value, что обычно подходит, если бэкенд уже возвращает правильный объект Python.

        # Если пустое
        if val is None or isinstance(val, str):
            return val
        # Если строка
        if isinstance(val, str):
            user_id = ((self.DEFAULT_MASK + str(self.userId))[-17:])
            return u'{}-{}'.format(user_id[0:2], user_id[2:18])
        # Если что-то иное
        elif self._is_string(val):
            user_id = ((self.DEFAULT_MASK + str(self.userId))[-17:])
            return u'{}-{}'.format(user_id[0:2], user_id[2:18])
        else:
            return str.fromtimestamp(float(val))

    def get_db_prep_value(self, val, *args, **kwargs):
        # Преобразование значений запроса в значения базы данных
        if val is None:
            if self.default == models.fields.NOT_PROVIDED:
                return None
            return self.default
        # Возвращаем значения в базу
        return int(time.mktime(val.timetuple()))

    def value_to_string(self, obj):
        # Преобразование значения поля для сериалайзера
        val = self._get_val_from_obj(obj)
        # Преобразование в читаемую форму
        return self.to_python(val).strftime(self.DEFAULT_DATETIME_FMT)

    def from_db_value(self, val, *args, **kwargs):
        # Преобразование значений базы данных в объекты Python
        return self.to_python(val)
