from django.urls import path

from .views.author import AuthorDetailView
from .views.book import BookDetailView, BookListView
from .views.genre import GenreDetailView, GenreListView
from .views.series import SeriesVersionDetailView

urlpatterns = [
    path("", BookListView.as_view(), name="books"),
    path("<int:pk>", BookDetailView.as_view(), name="book"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author"),
    path("series/<int:pk>", SeriesVersionDetailView.as_view(), name="series"),
    path("genres/", GenreListView.as_view(), name="genres"),
    path("genres/<int:pk>", GenreDetailView.as_view(), name="genre"),
]
