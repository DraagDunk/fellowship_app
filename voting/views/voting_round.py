from typing import ClassVar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView

from ..models.book_suggestion import BookSuggestion, Vote
from ..models.voting_round import VotingRound, VotingRoundForm


def is_manager(self: User):
    return self.membership.manager


def has_voted(self: User, voting_round: VotingRound):
    return self.votes.filter(book_suggestion__voting_round=voting_round).exists()


def can_still_suggest(self: User, voting_round: VotingRound):
    return (
        self.book_suggestions.filter(voting_round=voting_round).count()
        < voting_round.suggestions_per_user
    )


User.add_to_class("is_manager", is_manager)
User.add_to_class("has_voted", has_voted)
User.add_to_class("can_still_suggest", can_still_suggest)


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
        VotingRound.StateEnum.VOTING: "voting_round_voting.html",
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
        return context

    def get_template_names(self):
        return [self.template_map[self.object.state()]]

    def post(self, request, *args, **kwargs):
        book_ids = [int(book_id) for book_id in request.POST.getlist("books", [])]
        voting_round = self.get_object()
        if request.user.has_voted(voting_round):
            raise ValidationError(_("User has already voted!"))
        elif len(book_ids) != voting_round.votes_per_user:
            raise ValidationError(_("User has voted for too many or too few books!"))
        else:
            for book_id in book_ids:
                suggestion_obj = BookSuggestion.objects.get(pk=book_id)
                Vote.objects.create(user=request.user, book_suggestion=suggestion_obj)

        return self.get(request, *args, **kwargs)


class VotingRoundManagerDetailView(ManagerRequiredMixin, VotingRoundUserDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = True
        return context
