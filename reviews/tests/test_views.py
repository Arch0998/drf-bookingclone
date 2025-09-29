from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from hotels.models import Hotel, Location


class ReviewViewSimpleTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="guestuser", password="pass", role="guest"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", location=self.location, owner=self.user
        )
        self.client = APIClient()
    
    def test_review_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reviews:review-list")
        data = {"hotel_id": self.hotel.id, "rating": 5, "comment": "Super!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["comment"], "Super!")
    
    def test_review_create_unauthenticated(self):
        url = reverse("reviews:review-list")
        data = {"hotel_id": self.hotel.id, "rating": 4, "comment": "Nice!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
    
    def test_review_unique_per_user_hotel(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reviews:review-list")
        data = {"hotel_id": self.hotel.id, "rating": 5, "comment": "First!"}
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
