from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking
from hotels.models import Hotel, Room, RoomType, Location
from payments.models import Payment, PaymentStatus, PaymentType


class PaymentModelSimpleTest(TestCase):
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
    
    def test_create_payment(self):
        payment = Payment.objects.create(
            booking=self.booking,
            amount=100,
            status=PaymentStatus.PENDING,
            payment_type=PaymentType.PAYMENT,
            session_id="sess_123",
            session_url="https://stripe.com/session/123",
        )
        self.assertEqual(payment.booking, self.booking)
        self.assertEqual(payment.amount, 100)
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        self.assertEqual(payment.payment_type, PaymentType.PAYMENT)
        self.assertEqual(payment.session_id, "sess_123")
