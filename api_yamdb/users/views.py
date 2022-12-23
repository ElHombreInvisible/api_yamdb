from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_SERIVCE_EMAIL

from .models import User
from .permissions import IsAdminUser
from .serializers import (CheckConfirmationCodeSerializer,
                          SendConfirmationCodeSerializer, UserSerializer)


def create_and_send_confirmation(user):
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(email=user.email).update(
        confirmation_code=make_password(confirmation_code,
                                        salt=None,
                                        hasher='default'))
    mail_subject = 'Код подтверждения на Yamdb.ru'
    message = (f'Ваш код подтверждения: {confirmation_code},'
               f' username: {user.username}')
    send_mail(mail_subject, message, DEFAULT_SERIVCE_EMAIL, [user.email])


@api_view(['POST'])
def send_confirmation_code(request):
    username = request.data.get('username')
    email = request.data.get('email')
    print(request.data)
    serializer = SendConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = User.objects.get_or_create(username=username, email=email)
    create_and_send_confirmation(user[0])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed('Запрещенный метод')
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['patch', 'get'],
            permission_classes=(IsAuthenticated,), url_path='me')
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)
