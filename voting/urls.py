from django.urls import path

from .views.voting_round import VotingRoundCreateView, VotingRoundUserDetailView

urlpatterns = [
    path("add", VotingRoundCreateView.as_view(), name="voting_round_create"),
    path("<int:pk>", VotingRoundUserDetailView.as_view(), name="voting_round")
]