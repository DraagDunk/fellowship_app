from django.contrib import admin

from .models.voting_round import VotingRound
from .models.book_suggestion import BookSuggestion, Vote

@admin.register(VotingRound)
class VotingRoundAdmin(admin.ModelAdmin):
    list_display = ("club", "start_time")

@admin.register(BookSuggestion)
class BookSuggestionAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "voting_round")

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("book_suggestion", "user")