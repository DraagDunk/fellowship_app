from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


def is_manager(self: User):
    return self.membership.manager


User.add_to_class("is_manager", is_manager)


class ManagerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_manager():
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
