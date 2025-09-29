from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from bookings.serializers import BookingSerializer
from hotels.models import Room, Hotel, RoomType, Location


class BookingSerializerSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="owneruser", password="pass"
        )
        self.user = get_user_model().objects.create_user(
            username="simpleuser", password="pass"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Simple Hotel", location=self.location, owner=self.owner
        )
        self.room_type = RoomType.objects.create(
            name="Standard", description="", max_guests=2, size=20, bed_count=1
        )
        self.room = Room.objects.create(
            hotel=self.hotel, number="1", room_type=self.room_type, price=100
        )

    def test_serializer_valid(self):
        data = {
            "room_id": self.room.id,
            "check_in": timezone.now().date(),
            "check_out": timezone.now().date() + timezone.timedelta(days=1),
        }
        request = type("Request", (), {"user": self.user})()
        serializer = BookingSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        booking = serializer.save()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.status, "PENDING")
    
    def test_serializer_invalid_dates(self):
        data = {
            "room_id": self.room.id,
            "check_in": timezone.now().date() + timezone.timedelta(days=2),
            "check_out": timezone.now().date(),
        }
        request = type("Request", (), {"user": self.user})()
        serializer = BookingSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("check_out", serializer.errors)
