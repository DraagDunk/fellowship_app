from contextlib import contextmanager
from contextvars import ContextVar

from django.db import models

_current_club = ContextVar("current_club", default=None)


def get_current_club():
    """Return the Club of the currently authenticated user, or None."""
    return _current_club.get()


@contextmanager
def override_club(club):
    """
    Explicitly run code as a club. For management commands, Celery
    tasks, tests, or admin tooling:

        with override_club(club):
            Membership.objects.all()   # only that club's rows
    """
    token = _current_club.set(club)
    try:
        yield
    finally:
        _current_club.reset(token)


class ClubContextMiddleware:
    """
    Middleware that records the request user's club.

    settings.MIDDLEWARE (order matters -- must come AFTER auth):

        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'yourapp.scoping.ClubContextMiddleware',
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        club = None
        if user is not None and user.is_authenticated:
            try:
                club = user.membership.club      # via ClubMembership
            except user.membership.RelatedObjectDoesNotExist:
                club = None                       # user has no membership
        _current_club.set(club)
        try:
            return self.get_response(request)
        finally:
            _current_club.set(None)


class ClubQuerySet(models.QuerySet):
    def for_club(self, club):
        if club is None:
            return self.none()
        return self.filter(club=club)


class ClubManager(models.Manager):
    """
    Drop-in default manager. `Model.objects` now only ever returns rows
    belonging to the current request user's club.

    If no club is in context (shell, Celery, migrations), we FAIL CLOSED
    and return nothing. That is a deliberate security choice: forgetting
    to set the context is an error, not a data leak. Use
    `Model.all_objects` (unscoped) or `override_club(...)` explicitly when
    you genuinely need global access.
    """

    def get_queryset(self):
        club = get_current_club()
        print(club)
        if club is None:
            return ClubQuerySet(self.model, using=self._db).none()
        return ClubQuerySet(self.model, using=self._db).filter(club=club)

    @classmethod
    def make(cls, club_lookup="club", **manager_kwargs):
        """
        For models whose relation to Club is INDIRECT.

        Example: Match -> Team -> Club

            class Match(models.Model):
                team = models.ForeignKey(Team, on_delete=models.CASCADE)
                objects = ClubManager.make("team__club")
                all_objects = models.Manager()
        """
        manager = cls(**manager_kwargs)

        class _IndirectManager(cls):
            def get_queryset(self):
                club = get_current_club()
                qs = ClubQuerySet(self.model, using=self._db)
                if club is None:
                    return qs.none()
                return qs.filter(**{club_lookup: club})

        return _IndirectManager()