from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from bookings.models import Booking
from hotels.models import Hotel, Room, RoomType, Location
from payments.models import PaymentStatus, PaymentType


class PaymentViewMockTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="owneruser", password="pass", role="owner"
        )
        self.guest = get_user_model().objects.create_user(
            username="guestuser", password="pass", role="guest"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", location=self.location, owner=self.owner
        )
        self.room_type = RoomType.objects.create(
            name="Standard", description="", max_guests=2, size=20, bed_count=1
        )
        self.room = Room.objects.create(
            hotel=self.hotel, number="1", room_type=self.room_type, price=100
        )
        self.booking = Booking.objects.create(
            user=self.guest,
            room=self.room,
            check_in=timezone.now().date(),
            check_out=timezone.now().date() + timezone.timedelta(days=1),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.guest)

    @patch("payments.views.create_stripe_session")
    def test_create_payment_api(self, mock_create_stripe_session):
        mock_create_stripe_session.return_value = {
            "session_id": "sess_123",
            "session_url": "https://stripe.com/session/123",
            "amount": 100,
        }
        url = reverse("payments:payment-list")
        data = {
            "booking": self.booking.id,
            "payment_type": PaymentType.PAYMENT,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], PaymentStatus.PENDING)
        self.assertEqual(response.data["session_id"], "sess_123")
        self.assertEqual(
            response.data["session_url"], "https://stripe.com/session/123"
        )
