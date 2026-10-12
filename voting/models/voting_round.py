from datetime import timedelta
from enum import Enum

from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Count

from fellowship_app.club_scope import ClubManager

from clubs.models import Club


def in_one_week():
    return timezone.now() + timedelta(weeks=1)

def in_two_weeks():
    return timezone.now() + timedelta(weeks=2)

class VotingRound(models.Model):
    start_time = models.DateTimeField(_("Start time"), auto_now=False, auto_now_add=False, default=timezone.now)
    suggestions_end_time = models.DateTimeField(_("Suggestions end time"), auto_now=False, auto_now_add=False, default=in_one_week)
    voting_end_time = models.DateTimeField(_("Voting end time"), auto_now=False, auto_now_add=False, default=in_two_weeks)
    votes_per_user = models.PositiveIntegerField(_("Votes per user"))
    suggestions_per_user = models.PositiveIntegerField(_("Suggestions per user"))
    number_of_winners = models.PositiveIntegerField(_("Number of winners"))
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE, related_name="voting_rounds")

    objects = ClubManager()

    class StateEnum(Enum):
        NOT_STARTED = "not_started"
        SUGGESTIONS = "suggestions"
        VOTING = "voting"
        ENDED = "ended"
        UNKNOWN = "unknown"

    def state(self):
        match (self.start_time < timezone.now(),
               self.suggestions_end_time < timezone.now(),
               self.voting_end_time < timezone.now()):
            case (False, _, _):
                # Voting round has not started yet.
                return self.StateEnum.NOT_STARTED
            case (True, False, _):
                # Voting round is open to suggestions
                return self.StateEnum.SUGGESTIONS
            case (True, True, False):
                # Users are voting
                return self.StateEnum.VOTING
            case (True, True, True):
                # Voting has ended
                return self.StateEnum.ENDED
            case _:
                # What happened??
                return self.StateEnum.UNKNOWN

    def result(self):
        return self.book_suggestions.annotate(number_of_votes=Count("votes")).order_by("-number_of_votes")

    def get_absolute_url(self):
        return reverse_lazy("voting_round", kwargs={"pk": self.pk})

    def __str__(self):
        return _("{club} voting round {start_time}").format(club=self.club, start_time=self.start_time)
    



class VotingRoundForm(forms.ModelForm):

    class Meta:
        model = VotingRound
        fields = ("start_time", "suggestions_end_time", "voting_end_time", "suggestions_per_user", "votes_per_user", "number_of_winners", "club")
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "suggestions_end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "voting_end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            )
        }