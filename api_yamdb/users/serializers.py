import re

from django.db import models
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class SendConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all(), ),
        ])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError('Email должен быть не'
                                              ' более 254 символов')
        return value

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('Username должен быть не'
                                              ' более 150 символов')
        if value == 'me':
            raise serializers.ValidationError('Использовать имя пользователя'
                                              '"me" запрещенно')

        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
            raise serializers.ValidationError(('Не допустимые символы '
                                               'в имени пользователя.'))
        return value


class CheckConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    email = models.EmailField(max_length=254,
                              unique=True)

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',)
        model = User

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError('Email должен быть не'
                                              ' более 254 символов')
        return value

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('Username должен быть не'
                                              ' более 150 символов')
        if value == 'me':
            raise serializers.ValidationError('Использовать имя пользователя'
                                              '"me" запрещенно')
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
            raise serializers.ValidationError(('Не допустимые символы '
                                               'в имени пользователя.'))
        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('first_name должен быть не'
                                              ' более 150 символов')
        return value

    def validate_last_name(self, value):
        if len(value) > 150:
            raise exceptions.PermissionDenied('last_name должен быть не'
                                              ' более 150 символов')
        return value


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role', )
        model = User
        read_only_fields = ('role',)

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError('Email должен быть не'
                                              ' более 254 символов')
        return value

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('Username должен быть не'
                                              ' более 150 символов')
        if value == 'me':
            raise serializers.ValidationError('Использовать имя пользователя'
                                              '"me" запрещенно')
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
            raise serializers.ValidationError(('Не допустимые символы '
                                               'в имени пользователя.'))
        return value

    def validate_first_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('first_name должен быть не'
                                              ' более 150 символов')
        return value

    def validate_last_name(self, value):
        if len(value) > 150:
            raise serializers.ValidationError('last_name должен быть не'
                                              ' более 150 символов')
        return value
