from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet) #параметр basename обязательно должен быть указан в тех случаях, когда queryset однозначно не задан во вьюсете, а определён через метод get_queryset().
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
    )

urlpatterns = [
    path('v1/', include(router.urls)),
]

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