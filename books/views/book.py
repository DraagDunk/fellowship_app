from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import BookVersion


class BookListView(LoginRequiredMixin, ListView):
    template_name = "books.html"
    model = BookVersion
    context_object_name = "books"
