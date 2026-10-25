from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from ..models import BookVersion, BookVersionForm


class BookListView(LoginRequiredMixin, ListView):
    template_name = "books.html"
    model = BookVersion
    context_object_name = "books"


class BookDetailView(LoginRequiredMixin, DetailView):
    template_name = "book.html"
    model = BookVersion
    context_object_name = "book"


class BookCreateView(LoginRequiredMixin, CreateView):
    template_name = "book_create.html"
    model = BookVersion
    form_class = BookVersionForm
