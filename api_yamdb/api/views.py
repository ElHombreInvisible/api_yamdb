from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title, Review
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleSerializer
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AuthorOrReadOnly



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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = Title.objects.get(id=title_id)
        new_queryset = title.reviews
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = Review.objects.get(id=review_id)
        new_queryset = review.comments
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
