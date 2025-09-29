from django.test import TestCase

from users.serializers import UserRegisterSerializer


class UserRegisterSerializerSimpleTest(TestCase):
    def test_serializer_valid(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role": "owner",
            "password": "pass1234",
            "password2": "pass1234",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "owner")
        self.assertTrue(user.check_password("pass1234"))
    
    def test_serializer_password_mismatch(self):
        data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "role": "guest",
            "password": "pass1234",
            "password2": "wrongpass",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
