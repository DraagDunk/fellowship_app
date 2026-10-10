from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from ..models.voting_round import VotingRound, VotingRoundForm

def is_manager(self: User):
    return self.membership.manager

User.add_to_class('is_manager', is_manager)

class ManagerRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager():
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class VotingRoundCreateView(ManagerRequiredMixin, CreateView):
    model = VotingRound
    context_object_name = "round"
    template_name = "voting_round_create.html"
    form_class = VotingRoundForm