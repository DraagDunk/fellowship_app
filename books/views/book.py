from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import BookVersion


class BookListView(LoginRequiredMixin, ListView):
    template_name = "books.html"
    model = BookVersion
    context_object_name = "books"

class BookDetailView(LoginRequiredMixin, DetailView):
    template_name = "book.html"
    model = BookVersion
    context_object_name = "book"