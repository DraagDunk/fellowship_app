from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from views.shared.manager_required_mixin import ManagerRequiredMixin

from ..models.club import ClubMembership


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "homepage.html"

    def get_queryset(self):
        return self.request.user.clubs.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["club"] = self.get_queryset()
        return context


class ClubMembershipListView(ManagerRequiredMixin, ListView):
    model = ClubMembership
    template_name = "clubmemberships.html"
    context_object_name = "memberships"
