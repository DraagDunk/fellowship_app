from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from ..models import Genre


class GenreListView(LoginRequiredMixin, ListView):
    template_name = "genres.html"
    model = Genre
    context_object_name = "genres"


class GenreDetailView(LoginRequiredMixin, DetailView):
    template_name = "genre.html"
    model = Genre
    context_object_name = "genre"
