"""
Views for the book APIs
"""
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from core.models import Book
from book import serializers


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'author',
                OpenApiTypes.STR,
                description='Filter by Author',
            ),
            OpenApiParameter(
                'genre',
                OpenApiTypes.STR,
                description='Filter by Genre',
            ),
            OpenApiParameter(
                'condition',
                OpenApiTypes.STR,
                description='Filter by Condition',
            ),
            OpenApiParameter(
                'location',
                OpenApiTypes.STR,
                description='Filter by Location',
            ),
        ]
    )
)
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Book.objects.filter(available=True).order_by('-id')
        author = self.request.query_params.get('author')
        genre = self.request.query_params.get('genre')
        condition = self.request.query_params.get('condition')
        location = self.request.query_params.get('location')

        if author:
            queryset = queryset.filter(Q(author=author))
        if genre:
            queryset = queryset.filter(Q(genre=genre))
        if condition:
            queryset = queryset.filter(Q(condition=condition))
        if location:
            queryset = queryset.filter(Q(location=location))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserBooksListView(ListAPIView):
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
