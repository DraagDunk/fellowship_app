from datetime import timedelta

from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

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
    number_of_winners = models.PositiveIntegerField(_("Number of winners"))
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE, related_name="voting_rounds")

class VotingRoundForm(forms.ModelForm):

    class Meta:
        model = VotingRound
        fields = ("start_time", "suggestions_end_time", "voting_end_time", "votes_per_user", "number_of_winners", "club")
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