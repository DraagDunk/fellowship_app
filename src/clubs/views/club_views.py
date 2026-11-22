from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from views.shared.manager_required_mixin import ManagerRequiredMixin

from ..forms.club import ClubMembershipForm, EmailTemplate, WelcomeEmailForm
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


class ClubMembershipCreateView(ManagerRequiredMixin, CreateView):
    model = ClubMembership
    template_name = "clubmembership_create.html"
    form_class = ClubMembershipForm

    def form_valid(self, form=None):
        form.instance.club = self.request.user.membership.club
        return super().form_valid(form)

class WelcomeEmailView(ManagerRequiredMixin, UpdateView):
    model = EmailTemplate
    template_name = "welcome_email.html"
    form_class = WelcomeEmailForm

    def get_object(self, queryset=None):
        club = self.request.user.clubs.first()

        obj = EmailTemplate.objects.get(
            club=club,
        )

        return obj

    def get_success_url(self):
        return reverse_lazy("club_welcome_email")
