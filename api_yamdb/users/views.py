import random

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import (exceptions, filters, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdminUser, IsOwner
from .serializers import (AccountSerializer, CheckConfirmationCodeSerializer,
                          SendConfirmationCodeSerializer, UserSerializer)


def create_and_send_confirmation(username, email):
    confirmation_code = ''.join(map(str, random.sample(range(10), 6)))
    User.objects.filter(email=email).update(
        confirmation_code=make_password(confirmation_code,
                                        salt=None,
                                        hasher='default'))
    mail_subject = 'Код подтверждения на Yamdb.ru'
    message = (f'Ваш код подтверждения: {confirmation_code},'
               f' username: {username}')
    send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>', [email])


@api_view(['POST'])
def send_confirmation_code(request):
    username = request.data.get('username')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.email != email:
            return Response(
                {'Пользователь с таким именем уже существует'},
                status=status.HTTP_400_BAD_REQUEST)
        create_and_send_confirmation(username, email)
        serializer = SendConfirmationCodeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = SendConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user = serializer.save()
    create_and_send_confirmation(username, email)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if check_password(confirmation_code, user.confirmation_code):
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

    def get_serializer_class(self):
        if self.request.user.role == 'user' and self.request.method == 'PATCH':
            return AccountSerializer
        return UserSerializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise exceptions.MethodNotAllowed('Запрещенный метод')
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.method == 'PUT':
            raise exceptions.MethodNotAllowed('Запрещенный метод')
        return super().perform_update(serializer)

    @action(detail=False, methods=['patch', 'get'],
            permission_classes=(IsOwner,), url_path='me')
    def me(self, request):
        if request.method == 'PATCH':
            serializer = AccountSerializer(request.user,
                                           data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)


class AccountViewSet(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,
                     ):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        # queryset = User.objects.get(username=self.request.user)
        queryset = get_object_or_404(User, username=self.request.user)
        return queryset

    def perform_update(self, serializer):
        if self.request.method == 'DELETE':
            raise exceptions.MethodNotAllowed('Запрещенный метод')
        return super().perform_update(serializer)
