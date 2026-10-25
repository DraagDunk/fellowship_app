from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fellowship_app.club_scope import ClubManager


class Club(models.Model):
    uuid = models.UUIDField(
        primary_key=True, verbose_name=_("UUID"), default=uuid4, editable=False
    )
    name = models.CharField(max_length=100, verbose_name=_("name"))

    members = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("members"),
        through="ClubMembership",
        related_name="clubs",
    )

    def __str__(self):
        return self.name

    def managers(self):
        return get_user_model().objects.filter(
            membership__manager=True, membership__club=self
        )

    def regular_members(self):
        return get_user_model().objects.filter(
            membership__manager=False, membership__club=self
        )

    def current_suggestion_rounds(self):
        return self.voting_rounds.filter(
            start_time__lte=timezone.now(), suggestions_end_time__gt=timezone.now()
        )

    def current_voting_rounds(self):
        return self.voting_rounds.filter(
            suggestions_end_time__lte=timezone.now(), voting_end_time__gt=timezone.now()
        )

    def ended_voting_rounds(self):
        return self.voting_rounds.filter(voting_end_time__lte=timezone.now())

    def most_recent_ended_vote(self):
        return self.ended_voting_rounds().last()


class ClubMembership(models.Model):
    person = models.OneToOneField(
        get_user_model(),
        verbose_name=_("person"),
        on_delete=models.CASCADE,
        related_name="membership",
    )
    club = models.ForeignKey(
        Club,
        verbose_name=_("club"),
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    manager = models.BooleanField(verbose_name=_("manager"), default=False)

    objects = ClubManager()
