"""
URL mappings for the book app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from book import views


router = DefaultRouter()
router.register('books', views.BookViewSet)

app_name = 'book'

urlpatterns = [
    path('', include(router.urls)),
    path('my-books/', views.UserBooksListView.as_view(), name='my-books'),
    path(
        'book-interests/',
        views.BookInterestListCreateView.as_view(),
        name='book-interest-list-create'
    ),
    path(
        'book-interests/<int:pk>/choose-recipient/',
        views.BookInterestUpdateView.as_view(),
        name='choose-recipient'
    ),
]
