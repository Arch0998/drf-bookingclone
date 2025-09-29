from django.test import TestCase

from users.models import User


class UserModelSimpleTest(TestCase):
    def test_create_guest_user(self):
        user = User.objects.create_user(username="guestuser", password="pass")
        self.assertEqual(user.role, "guest")
        self.assertEqual(str(user), f"{user.username} (guest)")
    
    def test_create_owner_user(self):
        user = User.objects.create_user(
            username="owneruser", password="pass", role="owner"
        )
        self.assertEqual(user.role, "owner")
        self.assertEqual(str(user), f"{user.username} (owner)")
