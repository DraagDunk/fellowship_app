from fellowship_app.club_scope import ClubManager

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from books.models import BookCore
from clubs.models import Club

from .voting_round import VotingRound


class BookSuggestion(models.Model):
    book = models.ForeignKey(BookCore, verbose_name=_("Book"), on_delete=models.CASCADE, related_name="book_suggestions")
    voting_round = models.ForeignKey(VotingRound, verbose_name=_("Voting round"), on_delete=models.CASCADE, related_name="book_suggestions")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="book_suggestions")
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE, related_name="book_suggestions")

    objects = ClubManager()

    def get_absolute_url(self):
        return reverse_lazy("voting_round", kwargs={"pk": self.voting_round.pk})

    def __str__(self):
        return _("{book} for {vote} by {user}").format(book=self.book, vote=self.voting_round, user=self.user.get_full_name())

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book", "voting_round"], name="unique_book_per_voting_round")
        ]


class Vote(models.Model):
    book_suggestion = models.ForeignKey(BookSuggestion, verbose_name=_("Book suggestion"), on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="votes")
