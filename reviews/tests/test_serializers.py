from django.contrib.auth import get_user_model
from django.test import TestCase

from hotels.models import Hotel, Location
from reviews.serializers import ReviewSerializer


class ReviewSerializerSimpleTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="guestuser", password="pass", role="guest"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", location=self.location, owner=self.user
        )
    
    def test_serializer_valid(self):
        data = {"hotel_id": self.hotel.id, "rating": 5, "comment": "Awesome!"}
        request = type("Request", (), {"user": self.user})()
        serializer = ReviewSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        review = serializer.save()
        self.assertEqual(review.hotel, self.hotel)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
    
    def test_serializer_invalid_rating(self):
        data = {"hotel_id": self.hotel.id, "rating": 10, "comment": "Too high!"}
        request = type("Request", (), {"user": self.user})()
        serializer = ReviewSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)
