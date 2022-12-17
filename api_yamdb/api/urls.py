from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import send_confirmation_code, get_jwt_token


router = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/',
         send_confirmation_code,
         name='get_confirmation_code'),
    path('v1/auth/token/',
         get_jwt_token,
         name='get_jwt_token'),
    path('v1/', include(router.urls)),
]

