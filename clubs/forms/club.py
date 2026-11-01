from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from ..models.club import ClubMembership


class ClubMembershipForm(forms.ModelForm):
    email = forms.EmailField(required=True, label=_("Email"))

    first_name = forms.CharField(required=True, label=_("First name"))

    last_name = forms.CharField(required=True, label=_("Last name"))

    class Meta:
        model = ClubMembership
        fields = ("club", "person", "manager")

    def clean(self):
        cleaned = super().clean()

        # Create a user
        user = User.objects.create(
            username=cleaned.get("email"),
            email=cleaned.get("email"),
            first_name=cleaned.get("first_name"),
            last_name=cleaned.get("last_name"),
        )

        cleaned["person"] = user

        cleaned.pop("first_name")
        cleaned.pop("last_name")
        cleaned.pop("email")

        return cleaned
