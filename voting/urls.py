from django.urls import path

from .views.voting_round import VotingRoundCreateView

urlpatterns = [
    path("add", VotingRoundCreateView.as_view(), name="voting_round_create"),
]