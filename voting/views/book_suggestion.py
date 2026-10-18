from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from books.models import BookCore

from ..models.book_suggestion import BookSuggestion
from ..models.voting_round import VotingRound


class BookSuggestionCreateView(LoginRequiredMixin, CreateView):
    model = BookSuggestion
    template_name = "book_suggestion_create.html"

    fields = ("book",)

    def get(self, request, *args, **kwargs):
        if (
            request.user.book_suggestions.filter(voting_round=self.voting_round).count()
            < self.voting_round.suggestions_per_user
        ):
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied(
                _("User has already suggested {n} books.").format(
                    n=self.voting_round.suggestions_per_user
                )
            )

    def dispatch(self, request, *args, **kwargs):
        self.voting_round = get_object_or_404(VotingRound, pk=self.kwargs["round_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.voting_round = self.voting_round
        form.instance.user = self.request.user
        form.instance.club = self.voting_round.club
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["book"].queryset = BookCore.objects.exclude(
            book_suggestions__voting_round=self.voting_round
        )
        return form
