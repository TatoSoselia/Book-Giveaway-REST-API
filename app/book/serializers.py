"""
Serializers for book APIs
"""
from rest_framework import serializers

from core.models import (
    Book,
    Genre,
)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genres."""

    class Meta:
        model = Genre
        fields = ['id', 'name']
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for books."""

    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description',
            'available', 'location', 'condition', 'image',
            'genres',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        book = Book.objects.create(**validated_data)

        # Create genres or get existing ones based on genre names
        for genre_data in genres_data:
            genre_name = genre_data['name']
            genre, created = Genre.objects.get_or_create(name=genre_name)
            book.genres.add(genre)  # Add the genre to the book

        return book
