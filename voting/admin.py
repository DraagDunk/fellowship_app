from django.contrib import admin

from .models.voting_round import VotingRound
from .models.book_suggestion import BookSuggestion

@admin.register(VotingRound)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("club", "start_time")

@admin.register(BookSuggestion)
class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "voting_round")