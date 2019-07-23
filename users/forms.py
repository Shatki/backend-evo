#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import forms
from .models import User


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'userId',
            'first_name',
            'last_name',
        )
        readonly_fields = (
            'date_joined',
            'date_updated',)


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'is_admin',
            'user_permissions',
        )
