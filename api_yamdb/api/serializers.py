# api/serializers
from rest_framework import serializers

from users.models import User


class SendConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

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

        return value


class CheckConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name',
                  'last_name',
                  'username',
                  'bio',
                  'email',
                  'role',)
        model = User
