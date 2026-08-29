from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models.club import Club


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

    def get_queryset(self):
        return self.request.user.clubs.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["club"] = self.get_queryset()
        return context
    
    