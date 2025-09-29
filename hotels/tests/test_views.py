from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from hotels.models import Location


class HotelViewSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owneruser", password="pass", role="owner")
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.client = APIClient()
    
    def test_hotel_create_authenticated(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("hotels:hotel-list")
        data = {
            "name": "Test Hotel",
            "location": self.location.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Test Hotel")
        self.assertEqual(response.data["location"], self.location.id)
    
    def test_hotel_create_unauthenticated(self):
        url = reverse("hotels:hotel-list")
        data = {
            "name": "Test Hotel",
            "location": self.location.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
