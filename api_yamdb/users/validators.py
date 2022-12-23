import re

from rest_framework import serializers


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError('Использовать имя пользователя'
                                          '"me" запрещенно')
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise serializers.ValidationError(('Не допустимые символы '
                                           'в имени пользователя.'))
