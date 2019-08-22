# -*- coding: utf-8 -*-
import django.db.models as models
from django.utils.translation import gettext_lazy as _
from django.core import exceptions, checks


class UserId(object):
    """
        Класс индентификатора пользователя в облаке Эвотор. Используется как primary_key=True
    """
    DEFAULT_USERID = '01-000000000000001'
    DEFAULT_MASK = '00-000000000000000'
    REGEX_USERID = r'[0-9]{2}-[0-9]{15}'
    SEPARATOR_CONST = '-'
    MAX_NODE = 10**2
    MAX_NUMBER = 10**15
    MAX_INT = MAX_NODE * MAX_NUMBER

    def __init__(self, str=None, int=None, fields=None):
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

    @property
    def str(self):
        str = '%017d' % self.int
        return '%s-%s' % (str[:2], str[2:])

    def get_default(self):
        return UserId(str=self.DEFAULT_USERID)

    def __eq__(self, other):
        if isinstance(other, UserId):
            return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, UserId):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, UserId):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, UserId):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, UserId):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __getstate__(self):
        return {'int': self.int}

    def __setstate__(self, state):
        object.__setattr__(self, 'int', state['int'])

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UserId objects are immutable')

    def __unicode__(self):
        str = u'%017d' % self.int
        return u'%s-%s' % (str[:2], str[2:])

    def __str__(self):
        str = '%017d' % self.int
        return '%s-%s' % (str[:2], str[2:])


class UserIdField(models.Field):
    """
        ID field uses in evotor users' model
    """
    default_error_messages = {
        'invalid': _('“%(value)s” is not a valid UserID.'),
    }
    description = _('Universally Evotor unique user identifier')
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['max_length'] = 18
        kwargs['default'] = UserId.DEFAULT_USERID
        super(UserIdField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(UserIdField, self).check(**kwargs)
        errors.extend(self._check_primary_key())
        return errors

    def _check_primary_key(self):
        if not self.primary_key:
            return [
                checks.Error(
                    'UserIdFields must set primary_key=True.',
                    obj=self,
                    id='fields.E100',
                ),
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(UserIdField, self).deconstruct()
        kwargs['primary_key'] = True
        del kwargs['max_length'], kwargs['blank'], kwargs['default']
        return name, path, args, kwargs

    @staticmethod
    def internal_type():
        """
            Возвращает наименование поля данных для моделей

            :return: 'UserIdField'
        """
        return 'UserIdField'

    def db_type(self, connection):
        """
            Возвращает тип значения для базы данных, у MySQL это bigint

            :param connection: объект базы данных
            :return: 'bigint'
        """
        return 'bigint'

    def get_prep_value(self, value):
        """
            Метод должен вернуть значение, которое можно использовать как параметр в запросе.

            :param value: значение атрибута поля модели
            :return: Значение - параметр в запросе У нас это UserId
        """
        value = super(UserIdField, self).get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
            Преобразует value в значение для бэкенда базы данных.
            По умолчанию возвращает value, если prepared=True, иначе – результат get_prep_value()

            :param value: UserId значение для преобразования
            :param connection: объект WrappedDataBase
            :param prepared:
            :return: возвращает bigint значение из объекта python для базы данных
        """
        value = super(UserIdField, self).get_db_prep_value(value, connection, prepared)
        if not isinstance(value, UserId):
            value = self.to_python(value)
        # if value is None:
        #     cursor = connection.cursor()
        #     cursor.execute('SELECT max(userId) FROM users  DESC LIMIT 0, 1')
        #     result = cursor.fetchall()[0][0]
        #     return result + 1
        return value.int

    def to_python(self, value):
        """
            Преобразует значение из базы данных (или сериалайзера) в объект Python.
            Метод обратный get_prep_value() - подготавливает значение для поля для вставки в базу данных.
            По умолчанию возвращает value, что обычно подходит, если бэкенд уже возвращает правильный объект Python.

            Convert the input value into the expected Python data type, raising
            django.core.exceptions.ValidationError if the data can't be converted.
            Return the converted value. Subclasses should override this.

            :param value: получаемое значение для преобразование в объект python
            :return: всегда возвращает объект python типа UserId
        """
        if value is None or value == '':
             value = UserId.DEFAULT_USERID
        if not isinstance(value, UserId):
            input_form = 'int' if isinstance(value, int) else 'str'
            try:
                return UserId(**{input_form: value})
            except (AttributeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value

    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.has_auto_field, \
            "A model can't have more than one AutoField."
        super(UserIdField, self).contribute_to_class(cls, name, **kwargs)
        cls._meta.has_auto_field = True
        cls._meta.auto_field = self

    def from_db_value(self, value, *args, **kwargs):
        """
            Преобразование значений базы данных в объекты Python

            :param value: значение из базы
            :param args:
            :param kwargs:
            :return: возвращаем созданный или преобразованный объект python типа UserId
        """
        return self.to_python(value)
