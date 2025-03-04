from django.contrib import admin
from django.urls import path, include
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list"),
    path(
        "books/<int:pk>/", BookRetrieveUpdateDestroyView.as_view(), name="book-detail"
    ),
]
