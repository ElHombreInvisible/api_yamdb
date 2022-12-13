from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title
from rest_framework import filters, mixins, permissions, viewsets
# Create your views here.
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset=Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Genre.objects.all()
    serialzer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    serializer_class = TitleSerializer