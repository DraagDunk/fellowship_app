from django.urls import path

from .views.club_views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
]