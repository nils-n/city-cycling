from django.urls import path

from profiles.views import profile


urlpatterns = [
    path("", profile, name="profile"),
]
