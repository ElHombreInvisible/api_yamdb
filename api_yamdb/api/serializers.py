# api/serializers
from rest_framework import serializers

from users.models import User


class SendConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')


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

