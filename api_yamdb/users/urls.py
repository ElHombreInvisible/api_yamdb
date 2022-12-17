from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_jwt_token, send_confirmation_code

app_name = 'users'

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(user_router.urls)),
    path('auth/signup/',
         send_confirmation_code,
         name='get_confirmation_code'),
    path('auth/token/',
         get_jwt_token,
         name='get_jwt_token'),

    ]
