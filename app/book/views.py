"""
Views for the book APIs
"""
from rest_framework import viewsets, permissions
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
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
from core.models import Book, BookInterest
from book import serializers


class IsOwnerOrReadOnly(permissions.BasePermission):
    """custom permission to only allow owners to edit their own objects."""
    def has_object_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerForBook(permissions.BasePermission):
    """Custom permission to only allow owners to edit book-related objects."""
    def has_object_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.book.user == request.user


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
    """Manage book."""
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
            queryset = queryset.filter(genres__name__icontains=genre)
        if condition:
            queryset = queryset.filter(Q(condition=condition))
        if location:
            queryset = queryset.filter(Q(location=location))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserBooksListView(ListAPIView):
    """API endpoint for listing books owned by the authenticated user."""
    serializer_class = serializers.BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')


class BookInterestListCreateView(ListCreateAPIView):
    """API endpoint for listing and creating book interests."""
    queryset = BookInterest.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            # For creating book interests, use UserBookInterestSerializer
            return serializers.UserBookInterestSerializer
        else:
            # For listing book interests, use OwnerBookInterestSerializer
            return serializers.OwnerBookInterestSerializer

    def perform_create(self, serializer):
        serializer.save(interested_user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(book__user=self.request.user).order_by('-id')  # noqa: E501


class BookInterestUpdateView(UpdateAPIView):
    """API endpoint for updating book interests."""
    queryset = BookInterest.objects.all()
    serializer_class = serializers.OwnerBookInterestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerForBook]

    def perform_update(self, serializer):
        serializer.save(chosen_by_owner=True)
