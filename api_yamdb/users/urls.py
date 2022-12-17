from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import send_confirmation_code, get_jwt_token

app_name = 'users'

urlpatterns = [
    path('auth/signup/',
         send_confirmation_code,
         name='get_confirmation_code'),
    path('auth/token/',
         get_jwt_token,
         name='get_jwt_token'),
    ]
