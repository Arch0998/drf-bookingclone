from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


class UserViewSimpleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="pass1234",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role="guest",
        )
    
    def test_user_register(self):
        url = reverse("users:user-register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "role": "owner",
            "password": "newpass1234",
            "password2": "newpass1234",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["role"], "owner")
    
    def test_user_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)
    
    def test_user_profile_unauthenticated(self):
        url = reverse("users:user-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
