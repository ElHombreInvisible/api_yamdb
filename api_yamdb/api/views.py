from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Review
from api.serializers import ReviewSerializer, CommentSerializer
from api.permissions import AuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = PageNumberPagination

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
