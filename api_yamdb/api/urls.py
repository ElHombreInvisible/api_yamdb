from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from django.urls import include, path
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'v1/categories', CategoryViewSet)
router.register(r'v1/groups', GenreViewSet)
router.register(r'v1/titles', TitleViewSet) #параметр basename обязательно должен быть указан в тех случаях, когда queryset однозначно не задан во вьюсете, а определён через метод get_queryset().


urlpatterns = [
    path('', include(router.urls)),
]
