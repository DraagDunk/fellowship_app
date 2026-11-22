from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from views.shared.manager_required_mixin import ManagerRequiredMixin

from ..forms.club import ClubMembershipForm, ClubWelcomeEmailForm
from ..models.club import ClubEmailTemplate, ClubMembership


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

class ClubWelcomeEmailView(ManagerRequiredMixin, UpdateView):
    model = ClubEmailTemplate
    template_name = "welcome_email.html"
    form_class = ClubWelcomeEmailForm

    def get_object(self, queryset=None):
        club = self.request.user.membership.club

        template = ClubEmailTemplate.objects.get(
            club=club, 
            template_type=ClubEmailTemplate.EmailTemplateType.WELCOME
        )

        return template

    def get_success_url(self):
        return reverse_lazy("club_welcome_email")
