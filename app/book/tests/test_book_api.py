"""
Tests for Book APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Book

from book.serializers import BookSerializer


BOOKS_URL = reverse('book:book-list')


def create_book(user, **params):
    """Create and return a sample book."""
    defaults = {
        'title': 'sample title for book',
        'author': 'test auth',
        'description': 'sample description for book',
        'available': True,
        'location': 'test pickup_location',
        'condition': 'good',
        'image': 'testbook.jpg',
    }
    defaults.update(params)

    book = Book.objects.create(user=user, **defaults)
    return book


class PublicBookAPITests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        "test for a non-registered user to be able to view available books"
        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateBookApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_books(self):
        """Test retrieving a list of book."""
        create_book(user=self.user)
        create_book(user=self.user)

        res = self.client.get(BOOKS_URL)

        books = Book.objects.all().order_by('-id')
        serializer = BookSerializer(books, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self):
        """Test creating a book."""
        payload = {
            'title': 'test Book Title',
            'author': 'test Author Name',
            'description': 'test Description of the book',
            'available': True,
            'location': 'test Location',
            "genres": [
                {"name": "Genre1"},
                {"name": "Genre2"}
            ],
        }
        res = self.client.post(BOOKS_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data['id'])
        for k, v in payload.items():
            if k == 'genres':
                genre_names = [genre['name'] for genre in payload['genres']]
                self.assertEqual(
                    list(book.genres.values_list('name', flat=True)),
                    genre_names,
                )
            else:
                self.assertEqual(getattr(book, k), v)
        self.assertEqual(book.user, self.user)
