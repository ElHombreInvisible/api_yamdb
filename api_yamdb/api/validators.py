import datetime as dt

from rest_framework import serializers


def validate_year(data):
    if data > dt.datetime.now().year:
        raise serializers.ValidationError(
            'Неверная дата выхода или произведение еще не вышло.')
    return data
