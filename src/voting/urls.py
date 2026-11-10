from django.urls import path

from .views.book_suggestion import BookSuggestionCreateView
from .views.voting_round import (
    VotingRoundCreateView,
    VotingRoundListView,
    VotingRoundUserDetailView,
    VotingRoundVotingView,
)

urlpatterns = [
    path("", VotingRoundListView.as_view(), name="voting_rounds"),
    path("add", VotingRoundCreateView.as_view(), name="voting_round_create"),
    path("<int:pk>", VotingRoundUserDetailView.as_view(), name="voting_round"),
    path("<int:pk>/vote", VotingRoundVotingView.as_view(), name="voting_round_vote"),
    path(
        "<int:round_pk>/suggestions/add",
        BookSuggestionCreateView.as_view(),
        name="book_suggestion_create",
    ),
]
