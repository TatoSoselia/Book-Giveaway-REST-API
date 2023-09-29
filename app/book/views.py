"""
Views for the book APIs
"""
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from core.models import Book
from book import serializers


class BookViewSet(viewsets.ModelViewSet):
    """View for manage book APIs."""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(available=True).order_by('-id')

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class UserBooksListView(ListAPIView):
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
