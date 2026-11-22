from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
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
        blank=True,
    )
    club = models.ForeignKey(
        Club,
        verbose_name=_("club"),
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    manager = models.BooleanField(verbose_name=_("manager"), default=False)

    objects = ClubManager()

    def __str__(self):
        return _("{name} of {club}").format(
            name=self.person.get_full_name(), club=self.club.name
        )

    def get_absolute_url(self):
        return reverse_lazy("members")

class EmailTemplate(models.Model):
    DEFAULT_WELCOME_SUBJECT = "Velkommen til [[CLUB_NAME]]"
    DEFAULT_WELCOME_BODY = (
                    "Hej [[FIRST_NAME]],\n\n"
                    "Velkommen til [[CLUB_NAME]].\n\n"
                    "Opret dit password ved at besøge dette link:\n[[SET_PASSWORD_URL]]\n"
                    "Linket virker i et par dage.\n\n"
                    "Vi glæder os til at se dig til vores møder!\n\n"
                    "Venlig Hilsen,\n"
                    "[[CLUB_NAME]]"
                )

    # TODO: Add logic to these later
    TOKENS = {
        "FULL_NAME",
        "FIRST_NAME",
        "CLUB_NAME",
        "SET_PASSWORD_URL",
    }


    class EmailTemplateType(models.TextChoices):
        WELCOME = "welcome", "Velkommen"

    club = models.ForeignKey(
        Club,
        verbose_name=_("Email Templates"),
        on_delete=models.CASCADE,
        related_name="email_templates"
    )

    template_type = models.CharField(
        max_length=10,
        choices=EmailTemplateType.choices
    )

    # Does not accept django syntax. Only accepts defined replace tokens
    subject = models.CharField(max_length=255)

    # Does not accept django syntax. Only accepts defined replace tokens
    body = models.TextField(max_length=2000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["club", "template_type"], name="unqiue_club_template_type")
        ]
