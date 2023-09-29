"""
Serializers for book APIs
"""
from rest_framework import serializers

from core.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for books."""

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description',
            'available', 'pickup_location', 'condition', 'image',
        ]
        read_only_fields = ['id']
