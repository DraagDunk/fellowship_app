from typing import ClassVar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView, ListView

from views.shared.manager_required_mixin import ManagerRequiredMixin

from ..forms.voting_round import VotingRoundForm, VotingRoundVotingForm
from ..models.book_suggestion import BookSuggestion, Vote
from ..models.voting_round import VotingRound


def has_voted(self: User, voting_round: VotingRound):
    return self.votes.filter(book_suggestion__voting_round=voting_round).exists()


def can_still_suggest(self: User, voting_round: VotingRound):
    return (
        self.book_suggestions.filter(voting_round=voting_round).count()
        < voting_round.suggestions_per_user
    )


User.add_to_class("has_voted", has_voted)
User.add_to_class("can_still_suggest", can_still_suggest)


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
            return redirect(
                reverse_lazy("voting_round", kwargs={"pk": self.object_list.first().pk})
            )
        else:
            return response


class VotingRoundUserDetailView(LoginRequiredMixin, DetailView):
    model = VotingRound
    context_object_name = "round"

    template_map: ClassVar[dict[VotingRound.StateEnum, str]] = {
        VotingRound.StateEnum.NOT_STARTED: "voting_round_not_started.html",
        VotingRound.StateEnum.SUGGESTIONS: "voting_round_suggestions.html",
        VotingRound.StateEnum.VOTING: "voting_round_voted.html",
        VotingRound.StateEnum.ENDED: "voting_round_ended.html",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = False
        user_has_voted = self.request.user.has_voted(self.object)
        context["has_voted"] = user_has_voted
        if user_has_voted:
            context["voted_suggestions"] = BookSuggestion.objects.filter(
                votes__user=self.request.user
            ).values_list("pk", flat=True)
        context["can_still_suggest"] = self.request.user.can_still_suggest(self.object)
        user_votes = Vote.objects.filter(
            book_suggestion=OuterRef("pk"), user=self.request.user
        )
        context["suggestions"] = self.object.book_suggestions.all().annotate(
            own=Q(user=self.request.user), voted_for=Exists(user_votes)
        )
        return context

    def get_template_names(self):
        return [self.template_map[self.object.state()]]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if (
            self.object.state() == VotingRound.StateEnum.VOTING
            and not request.user.has_voted(self.object)
        ):
            return redirect(
                reverse_lazy("voting_round_vote", kwargs={"pk": self.object.pk})
            )
        return response


class VotingRoundVotingView(LoginRequiredMixin, FormView):
    template_name = "voting_round_voting.html"
    form_class = VotingRoundVotingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["round"] = self.voting_round
        return context

    def dispatch(self, request, *args, **kwargs):
        self.voting_round = get_object_or_404(VotingRound, pk=kwargs.get("pk"))
        if request.user.has_voted(self.voting_round):
            raise PermissionDenied(_("User already voted!"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["voting_round"] = self.voting_round
        return kwargs

    def form_valid(self, form: VotingRoundVotingForm):
        form.save(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("voting_round", kwargs={"pk": self.voting_round.pk})


class VotingRoundManagerDetailView(ManagerRequiredMixin, VotingRoundUserDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = True
        return context
