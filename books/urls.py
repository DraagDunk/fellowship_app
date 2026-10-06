from django.urls import path

from .views.book import BookListView

urlpatterns = [
    path("", BookListView.as_view(), name="books")
]