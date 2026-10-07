from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Genre


class GenreListView(LoginRequiredMixin, ListView):
    template_name = "genres.html"
    model = Genre
    context_object_name = "genres"

class GenreDetailView(LoginRequiredMixin, DetailView):
    template_name = "genre.html"
    model = Genre
    context_object_name = "genre"