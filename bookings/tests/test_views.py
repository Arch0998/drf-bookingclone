from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from hotels.models import Hotel, Room, RoomType, Location


class BookingViewSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owneruser", password="pass")
        self.user = get_user_model().objects.create_user(username="simpleuser", password="pass")
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(name="Simple Hotel", location=self.location, owner=self.owner)
        self.room_type = RoomType.objects.create(name="Standard", description="", max_guests=2, size=20, bed_count=1)
        self.room = Room.objects.create(hotel=self.hotel, number="1", room_type=self.room_type, price=100)
        self.client = APIClient()
    
    def test_booking_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("bookings:booking-list")
        data = {
            "room_id": self.room.id,
            "check_in": timezone.now().date(),
            "check_out": timezone.now().date() + timezone.timedelta(days=1),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "PENDING")
        self.assertEqual(response.data["user"]["id"], self.user.id)
    
    def test_booking_create_unauthenticated(self):
        url = reverse("bookings:booking-list")
        data = {
            "room_id": self.room.id,
            "check_in": timezone.now().date(),
            "check_out": timezone.now().date() + timezone.timedelta(days=1),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)
