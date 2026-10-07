from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Author

class AuthorDetailView(LoginRequiredMixin, DetailView):
    template_name = "author.html"
    model = Author
    context_object_name = "author"