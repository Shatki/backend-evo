# -*- coding: utf-8 -*-
import django.db.models as models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


class UserId(object):
    """

    """
    DEFAULT_USERID = '01-0000000000000001'
    DEFAULT_MASK = '00-000000000000000'
    PATTERN_USERID = r'[0-9]{2}-[0-9]{15}'
    SEPARATOR_CONST = '-'
    MAX_NODE = 10**2
    MAX_NUMBER = 10**15
    MAX_INT = MAX_NODE * MAX_NUMBER

    def __init__(self, str=None, int=None, fields=None,):
        """
            Создаем UserID
            Примеры:
                UserID('01-0000000000012345')
                UserID(fields=('01', '0000000000012345')


            UserIds have these read-only attributes:

                fields      a tuple of the two integer fields of the UserId,
                            which are also available as two individual attributes
                            and two derived attributes:
                    node                    the first 32 bits of the UserId
                    number                  the next 16 bits of the UserId

                str         the UUID as a 18-character decimal string
                int         the UUID as a long integer

        """
        # должен быть получен только один из аргументов
        if [str, int, fields].count(None) != 2:
            raise TypeError('one of the str, fields, '
                            'or int arguments must be given')

        # Если получили fields
        if fields is not None:
            if len(fields) != 2:
                raise ValueError('fields is not a 2-tuple')
            (node, number) = fields
            if not 0 < node < self.MAX_NODE:
                raise ValueError('field 1 out of range (must be between 1 and 99)')
            if not 0 < number < self.MAX_NUMBER:
                raise ValueError('field 1 out of range (must be between 1 and 10**15-1)')
            int = node * self.MAX_NUMBER + number

        if str is not None:
            # TODO: В третьей версии питона переделать long на int
            int = long(str.replace(self.SEPARATOR_CONST, "").lstrip('0'))

        if int is not None:
            if not 0 < int < self.MAX_INT:
                raise ValueError('int is out of range (must be between 1 and 10**17-1)')

        object.__setattr__(self, 'int', int)

    @property
    def node(self):
        return '%017d' % self.int[:2]

    @property
    def number(self):
        return '%017d' % self.int[2:]

    @property
    def fields(self):
        str = '%017d' % self.int
        return str[0:2], str[2:18]

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UserId objects are immutable')

    def __str__(self):
        str = '%017d' % self.int
        return '%s-%s' % (str[:2], str[2:])

    def default(self):
        return UserId(str=self.DEFAULT_USERID)


class UserIdField(models.Field):
    """
        ID field uses in evotor users' model
    """
    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid UserID.'),
    }
    description = _('Universally Evotor unique user identifier')
    empty_strings_allowed = False

    DEFAULT_MASK = '00-000000000000000'
    PATTERN_USERID = r'[0-9]{2}-[0-9]{15}'
    SEPARATOR_CONST = '-'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        super(UserIdField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        print 'deconstruct'
        name, path, args, kwargs = super(UserIdField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def get_internal_type(self):
        print 'get_internal_type'
        return 'UserIdField'

    def get_prep_value(self, value):
        print 'get_prep_value: ', value
        value = super(UserIdField, self).get_prep_value(value)
        if value is None:
            return None

        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
            Convert value to db UserId BigInteger before save
        """
        # Преобразует val в значение для бэкенда базы данных. По умолчанию возвращает value,
        # если prepared=True, иначе – результат get_prep_value()
        print 'get_db_prep_value: ', value
        if value is None:
            return None
        if re.match(self.PATTERN_USERID, value) and len(value) == 18:
            # Возвращаем значения в базу
            return value.replace('-', "").lstrip('0')
        return str(value)

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

    def value_to_string(self, obj):
        # Преобразование значения поля для сериалайзера
        print 'value_to_string: ', obj, self.get_val_from_obj(obj)
        # obj: 01-000000000738894 <class 'users.models.User'>
        # val: 01-000000000738894 <type 'unicode'>
        # Преобразование в читаемую форму
        return str(self.value_from_object(obj))

    def from_db_value(self, val, *args, **kwargs):
        print 'from_db_value: ', val, self.to_python(val)
        # Преобразование значений базы данных в объекты Python
        return self.to_python(val)


print UserId(fields=(1, 12345))
print UserId(str='01-000000000023456')
print UserId(int=1000000000034567)

print UserId.fields
