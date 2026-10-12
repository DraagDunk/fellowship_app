from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ..models.book_suggestion import BookSuggestion
from ..models.voting_round import VotingRound

class BookSuggestionCreateView(LoginRequiredMixin, CreateView):
    model = BookSuggestion
    template_name = "book_suggestion_create.html"

    fields = ("book",)

    def dispatch(self, request, *args, **kwargs):
        self.voting_round = get_object_or_404(VotingRound, pk=self.kwargs["round_pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.voting_round = self.voting_round
        form.instance.user = self.request.user
        form.instance.club = self.voting_round.club
        return super().form_valid(form)