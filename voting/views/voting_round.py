from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from ..models.voting_round import VotingRound, VotingRoundForm

def is_manager(self: User):
    return self.membership.manager

User.add_to_class('is_manager', is_manager)

class ManagerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager():
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class VotingRoundCreateView(ManagerRequiredMixin, CreateView):
    model = VotingRound
    template_name = "voting_round_create.html"
    form_class = VotingRoundForm

class VotingRoundListView(LoginRequiredMixin, ListView):
    model = VotingRound
    context_object_name = "rounds"
    template_name = "voting_round_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(start_time__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if len(self.object_list) == 1:
            return redirect(reverse_lazy("voting_round", kwargs={"pk": self.object_list.first().pk}))
        else:
            return response


class VotingRoundUserDetailView(LoginRequiredMixin, DetailView):
    model = VotingRound
    context_object_name = "round"

    template_map = {
        VotingRound.StateEnum.NOT_STARTED: "voting_round_not_started.html",
        VotingRound.StateEnum.SUGGESTIONS: "voting_round_suggestions.html",
        VotingRound.StateEnum.VOTING: "voting_round_voting.html",
        VotingRound.StateEnum.ENDED: "voting_round_ended.html"
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = False
        return context

    def get_template_names(self):
        return [self.template_map[self.object.state()]]


class VotingRoundManagerDetailView(ManagerRequiredMixin, VotingRoundUserDetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = True
        return context
    
