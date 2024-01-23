from django.urls import path

from profiles.views import profile, order_history, delete_profile


urlpatterns = [
    path("", profile, name="profile"),
    path("order_history/<order_number>", order_history, name="order_history"),
    path("delete/<int:user_id>", delete_profile, name="delete_profile"),
]
