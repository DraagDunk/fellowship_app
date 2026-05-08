from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Club(models.Model):
    uuid = models.UUIDField(primary_key=True, verbose_name=_("UUID"), default=uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name=_("name"))

    members = models.ManyToManyField(get_user_model(), verbose_name=_("members"), through="ClubMembership", related_name="clubs")


class ClubMembership(models.Model):
    person = models.ForeignKey(get_user_model(), verbose_name=_("person"), on_delete=models.CASCADE, related_name="memberships")
    club = models.ForeignKey(Club, verbose_name=_("club"), on_delete=models.CASCADE, related_name="memberships")

    manager = models.BooleanField(verbose_name=_("manager"), default=False)

