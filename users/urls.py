from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import UserRegisterView, UserProfileView

app_name = "users"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("me/", UserProfileView.as_view(), name="user-profile"),
]
