from django import forms
from django.utils.translation import gettext_lazy as _

from ..models.book_suggestion import BookSuggestion, Vote
from ..models.voting_round import VotingRound


class VotingRoundForm(forms.ModelForm):
    class Meta:
        model = VotingRound
        fields = (
            "start_time",
            "suggestions_end_time",
            "voting_end_time",
            "suggestions_per_user",
            "votes_per_user",
            "number_of_winners",
            "club",
        )
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "suggestions_end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "voting_end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class BookSuggestionSelectWidget(forms.CheckboxSelectMultiple):
    template_name = "widgets/voting_options.html"
    option_template_name = "widgets/voting_option.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        for option in context["widget"]["optgroups"]:
            _, opts, _ = option
            for opt in opts:
                opt["book"] = opt["value"].instance.book
        return context


class VotingRoundVotingForm(forms.Form):
    suggestions = forms.ModelMultipleChoiceField(
        BookSuggestion.objects.none(),
        required=True,
        label=_("Select the books you want to vote for"),
        widget=BookSuggestionSelectWidget,
    )

    def __init__(self, *args, voting_round: VotingRound | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.voting_round = voting_round
        self.fields["suggestions"].queryset = BookSuggestion.objects.filter(
            voting_round=voting_round
        )

    def clean_suggestions(self):
        suggestions = self.cleaned_data["suggestions"]
        if suggestions.count() != self.voting_round.votes_per_user:
            raise forms.ValidationError(
                _("You must vote for exactly {n} books!").format(
                    n=self.voting_round.votes_per_user
                )
            )
        return suggestions

    def save(self, user):
        return Vote.objects.bulk_create(
            [
                Vote(book_suggestion=suggestion, user=user)
                for suggestion in self.cleaned_data["suggestions"]
            ]
        )
