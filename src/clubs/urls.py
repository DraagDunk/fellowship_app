from django.urls import path

from .views.club_views import (
    ClubMembershipCreateView,
    ClubMembershipListView,
    ClubWelcomeEmailUpdateView,
    HomePageView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("members", ClubMembershipListView.as_view(), name="members"),
    path("members/add", ClubMembershipCreateView.as_view(), name="member_create"),
    path("settings/welcome-email/", ClubWelcomeEmailUpdateView.as_view(), name="club_welcome_email_edit")
]
