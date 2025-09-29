from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking
from hotels.models import Room, Hotel, RoomType, Location


class BookingModelSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owneruser", password="pass")
        self.user = get_user_model().objects.create_user(username="simpleuser", password="pass")
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(name="Simple Hotel", location=self.location, owner=self.owner)
        self.room_type = RoomType.objects.create(name="Standard", description="", max_guests=2, size=20, bed_count=1)
        self.room = Room.objects.create(hotel=self.hotel, number="1", room_type=self.room_type, price=100)
    
    def test_create_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=timezone.now().date(),
            check_out=timezone.now().date() + timezone.timedelta(days=1)
        )
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.status, "PENDING")
    
    def test_booking_str(self):
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=timezone.now().date(),
            check_out=timezone.now().date() + timezone.timedelta(days=1)
        )
        self.assertIn(str(self.user.username), str(booking))
        self.assertIn(str(self.hotel.name), str(booking))
