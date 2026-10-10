from django.db import models
from django.utils.translation import gettext_lazy as _

from clubs.models import Club


class VotingRound(models.Model):
    start_time = models.DateTimeField(_("Start time"), auto_now=False, auto_now_add=False)
    suggestions_end_time = models.DateTimeField(_("Suggestions end time"), auto_now=False, auto_now_add=False)
    voting_end_time = models.DateTimeField(_("Voting end time"), auto_now=False, auto_now_add=False)
    votes_per_user = models.PositiveIntegerField(_("Votes per user"))
    number_of_winners = models.PositiveIntegerField(_("Number of winners"))
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE, related_name="voting_rounds")