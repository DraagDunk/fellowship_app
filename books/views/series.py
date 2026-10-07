from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import SeriesVersion

class SeriesVersionDetailView(LoginRequiredMixin, DetailView):
    template_name = "series.html"
    model = SeriesVersion
    context_object_name = "series"