import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from ..models.club import ClubMembership, EmailTemplate


class ClubMembershipForm(forms.ModelForm):
    email = forms.EmailField(required=True, label=_("Email"))

    first_name = forms.CharField(required=True, label=_("First name"))

    last_name = forms.CharField(required=True, label=_("Last name"))

    class Meta:
        model = ClubMembership
        fields = ("person", "manager")
        widgets = {"person": forms.HiddenInput()}

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

class WelcomeEmailForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ["subject", "body"]

    VALID_TOKENS_REGULAR_EXPRESSION = re.compile(r"\[\[(.*?)\]\]", re.DOTALL)
    DJANGO_SYNTAX_REGULAR_EXPRESSION = re.compile(r"{{|}}|{%|%}|{#|#}")
    ILLEGAL_STRUCTURES = ["{{", "}}", "{%", "%}", "{#", "#}"]

    @staticmethod
    def validate_text(field, text):
        if WelcomeEmailForm.DJANGO_SYNTAX_REGULAR_EXPRESSION.search(text):
            raise forms.ValidationError(
                _("The {field} contains an illegal block structure. Please remove it. Illegal structures: {blocks}").format(
                    field=field,
                    blocks=", ".join(WelcomeEmailForm.ILLEGAL_STRUCTURES),
                )
            )
        for token in WelcomeEmailForm.VALID_TOKENS_REGULAR_EXPRESSION.findall(text):
            if token not in EmailTemplate.TOKENS:
                raise forms.ValidationError(
                    _("The {field} contains an illegal token '{token}'. Please remove it. Legal tokens: {legal}").format(
                        field=field,
                        token=token,
                        legal=", ".join(sorted(EmailTemplate.TOKENS))
                    )
                )
        return text

    def clean_subject(self):
        return WelcomeEmailForm.validate_text("subject", self.cleaned_data["subject"])

    def clean_body(self):
        return WelcomeEmailForm.validate_text("body", self.cleaned_data["body"])
