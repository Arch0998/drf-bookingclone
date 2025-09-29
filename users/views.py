from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from users.models import User
from users.serializers import UserRegisterSerializer


@extend_schema(
    tags=["Users"],
    summary="User registration endpoint",
    description="""
    Register a new user account.
    Required fields: username, email, password, password2.
    Optional: first_name, last_name, role (default: guest).
    Returns the created user data (without password fields).
    """,
    request=UserRegisterSerializer,
    responses={201: UserRegisterSerializer},
)
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["Users"],
    summary="Get current user profile",
    description="""
    Retrieve the profile of the currently authenticated user.
    Returns user data (id, username, email, first_name, last_name, role).
    """,
    responses={200: UserRegisterSerializer},
)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
