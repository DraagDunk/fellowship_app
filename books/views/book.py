from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from ..models import BookVersion


class BookListView(LoginRequiredMixin, ListView):
    template_name = "books.html"
    model = BookVersion
    context_object_name = "books"


class BookDetailView(LoginRequiredMixin, DetailView):
    template_name = "book.html"
    model = BookVersion
    context_object_name = "book"
