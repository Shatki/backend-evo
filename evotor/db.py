# -*- coding: utf-8 -*-
from django import forms
import django.db.models as models
from django.utils.translation import gettext_lazy as _
from django.core import checks, exceptions, validators


class UserId(object):
    """

    """
    DEFAULT_USERID = '01-000000000000001'
    DEFAULT_MASK = '00-000000000000000'
    REGEX_USERID = r'[0-9]{2}-[0-9]{15}'
    SEPARATOR_CONST = '-'
    MAX_NODE = 10**2
    MAX_NUMBER = 10**15
    MAX_INT = MAX_NODE * MAX_NUMBER

    def __init__(self, get_str=None, get_int=None, fields=None):
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
        if [get_str, get_int, fields].count(None) != 2:
            raise TypeError('one of the get_str, fields, '
                            'or get_int arguments must be given')

        # Если получили fields
        if fields is not None:
            if len(fields) != 2:
                raise ValueError('fields is not a 2-tuple')
            (node, number) = fields
            if not 0 < node < self.MAX_NODE:
                raise ValueError('field 1 out of range (must be between 1 and 99)')
            if not 0 < number < self.MAX_NUMBER:
                raise ValueError('field 1 out of range (must be between 1 and 10**15-1)')
            get_int = node * self.MAX_NUMBER + number

        if get_str is not None:
            # TODO: В третьей версии питона переделать long на int
            get_int = long(get_str.replace(self.SEPARATOR_CONST, "").lstrip('0'))

        if get_int is not None:
            if not 0 < get_int < self.MAX_INT:
                raise ValueError('get_int is out of range (must be between 1 and 10**17-1)')

        object.__setattr__(self, 'get_int', get_int)

    @property
    def node(self):
        return '%017d' % self.get_int[:2]

    @property
    def number(self):
        return '%017d' % self.get_int[2:]

    @property
    def fields(self):
        get_str = '%017d' % self.get_int
        return get_str[0:2], get_str[2:18]

    @property
    def get_str(self):
        get_str = '%017d' % self.get_int
        return '%s-%s' % (get_str[:2], get_str[2:])

    def from_default(self):
        return UserId(get_str=self.DEFAULT_USERID)

    def __eq__(self, other):
        if isinstance(other, UserId):
            return self.get_int == other.get_int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, UserId):
            return self.get_int < other.get_int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, UserId):
            return self.get_int > other.get_int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, UserId):
            return self.get_int <= other.get_int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, UserId):
            return self.get_int >= other.get_int
        return NotImplemented

    def __hash__(self):
        return hash(self.get_int)

    def __int__(self):
        return self.get_int

    def __getstate__(self):
        return {'get_int': self.get_int}

    def __setstate__(self, state):
        object.__setattr__(self, 'get_int', state['get_int'])

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UserId objects are immutable')

    def __unicode__(self):
        get_str = u'%017d' % self.get_int
        return u'%s-%s' % (get_str[:2], get_str[2:])

    def __str__(self):
        get_str = '%017d' % self.get_int
        return '%s-%s' % (get_str[:2], get_str[2:])


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
        kwargs['blank'] = True
        kwargs['max_length'] = 18
        super(UserIdField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UserIdField, self).deconstruct()
        kwargs['primary_key'] = True
        del kwargs['max_length'], kwargs['blank']
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'UserIdField'

    def db_type(self, connection):
        return 'bigint'

    def get_prep_value(self, value):
        value = super(UserIdField, self).get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
            Convert value to db UserId BigInteger before save
        """
        # Преобразует value в значение для бэкенда базы данных. По умолчанию возвращает value,
        # если prepared=True, иначе – результат get_prep_value()
        value = super(UserIdField, self).get_db_prep_value(value, connection, prepared)
        print value, type(value)
        if value is None:
            return None
        if not isinstance(value, UserId):
            value = self.to_python(value)
        print value.get_int
        return value.get_int

    def to_python(self, value):
        """
            Convert the input value into the expected Python data type, raising
            django.core.exceptions.ValidationError if the data can't be converted.
            Return the converted value. Subclasses should override this.
        """
        # Преобразует значение из базы данных (или сериалайзера) в объект Python.
        # Метод обратный get_prep_value() - подготавливает значение для поля для вставки в базу данных.
        #
        # По умолчанию возвращает value, что обычно подходит, если бэкенд уже возвращает правильный объект Python.
        if value is not None and not isinstance(value, UserId):
            input_form = 'get_int' if isinstance(value, int) else 'get_str'
            try:
                return UserId(**{input_form: value})
            except (AttributeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def from_db_value(self, value, *args, **kwargs):
        # Преобразование значений базы данных в объекты Python
        return self.to_python(value)
