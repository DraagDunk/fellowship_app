from django import forms

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
