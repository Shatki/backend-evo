#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator, ValidationError


def validator_numerator(value):
    a = value[0:2]  # Первые две буквы
    n = value[3:10]  # Последние 7 цифр
    if value[2] != '-':
        raise ValidationError(u'%s не корректный номер заказа' % value)
    if not (a.isalpha() & a.isupper()):
        raise ValidationError(u'%s укажите первые две заглавные буквы кода' % value)
    if not n.isdigit():
        raise ValidationError(u'%s укажите цифровой номер заказа' % value)


def validator_path(string):
    for s_ in string:
        if s_ == ' ':
            raise ValidationError(u'В строке "%s" замените пробелы символом подчеркивания!' % string)
        if ord('a') <= ord(s_) <= ord('z') or ord('A') <= ord(s_) <= ord('Z') or s_ == '_':
            pass
        else:
            # print(ord('a'), ord(s_), ord('z'), s_)
            raise ValidationError(u'В строке "%s" привутствуют запрещенные символы!' % string)


def validator_warranty(value):
    if value < 0:
        raise ValidationError(u'%i - не может быть верным гарантийным сроком ' % value)
    if value > 60:
        raise ValidationError(u'%i - слишком большой гарантийный срок' % value)


login = RegexValidator(r'^[\w.@+-]+$', message='Enter a valid username. '
                                               'This value may contain only letters, numbers and [@/./+/-] characters.')
numeric = RegexValidator(r'^[0-9]*$', message=u'допустимы только цифровые символы.')
alpha_all = RegexValidator(r'^[a-zA-Zа-яА-Я]*$', message=u'допустимы только буквенные символы.')
alpha_lat = RegexValidator(r'^[a-zA-Z]*$', message=u'допустимы только латинские буквы.')
hexnumeric = RegexValidator(r'^[0-9a-fA-F]*$', message=u'должен указывается в шестнадцатиричной системе.')
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=u'только буквенноцифровые символы допустимы.')
phone = RegexValidator(regex=r'^\+?1?\d{11}$',
                       message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
email = RegexValidator(regex='\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*', message='Enter a valid e-mail')
