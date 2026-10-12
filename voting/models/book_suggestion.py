from fellowship_app.club_scope import ClubManager

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from books.models import BookCore
from clubs.models import Club

from .voting_round import VotingRound


class BookSuggestion(models.Model):
    book = models.ForeignKey(BookCore, verbose_name=_("Book"), on_delete=models.CASCADE, related_name="book_suggestions")
    voting_round = models.ForeignKey(VotingRound, verbose_name=_("Voting round"), on_delete=models.CASCADE, related_name="book_suggestions")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="book_suggestions")
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE, related_name="book_suggestions")

    objects = ClubManager()

class Vote(models.Model):
    book_suggestion = models.ForeignKey(BookSuggestion, verbose_name=_("Book suggestion"), on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="votes")

    objects = ClubManager()