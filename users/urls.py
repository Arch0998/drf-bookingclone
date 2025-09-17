from django.urls import path

from users.views import UserRegisterView, UserProfileView

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("me/", UserProfileView.as_view(), name="user-profile"),
]
