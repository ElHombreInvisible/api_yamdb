from rest_framework import serializers
from users.models import User

from .validators import validate_username


class SendConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        max_length=254,
        required=True,)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        username = data['username']
        print(username)
        email = data['email']
        if (User.objects.filter(username=username)
            .exclude(email=email).exists()
           or User.objects.filter(email=email)
           .exclude(username=username).exists()):
            raise serializers.ValidationError('Неверные учетные данные')
        return data

    def validate_username(self, value):
        validate_username(value)
        return value


class CheckConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role',)
        model = User

    def validate_username(self, value):
        validate_username(value)
        return value
