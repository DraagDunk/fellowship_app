from django.urls import path

from .views.book import BookListView, BookDetailView
from .views.author import AuthorDetailView

urlpatterns = [
    path("", BookListView.as_view(), name="books"),
    path("<int:pk>", BookDetailView.as_view(), name="book"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author")
]