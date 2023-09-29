"""
Views for the book APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.models import Book
from book import serializers


class BookViewSet(viewsets.ModelViewSet):
    """View for manage book APIs."""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user).order_by('-id')
        else:
            return self.queryset.filter(available=True).order_by('-id')
