from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Club(models.Model):
    uuid = models.UUIDField(primary_key=True, verbose_name=_("UUID"), default=uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name=_("name"))

    members = models.ManyToManyField(get_user_model(), verbose_name=_("members"), through="ClubMembership", related_name="clubs")

    def __str__(self):
        return self.name

    def managers(self):
        return get_user_model().objects.filter(memberships__manager=True, memberships__club=self)

    def regular_members(self):
        return get_user_model().objects.filter(memberships__manager=False, memberships__club=self)


class ClubMembership(models.Model):
    person = models.OneToOneField(get_user_model(), verbose_name=_("person"), on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey(Club, verbose_name=_("club"), on_delete=models.CASCADE, related_name="memberships")

    manager = models.BooleanField(verbose_name=_("manager"), default=False)

