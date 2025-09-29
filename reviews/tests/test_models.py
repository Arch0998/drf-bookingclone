from django.contrib.auth import get_user_model
from django.test import TestCase

from hotels.models import Hotel, Location
from reviews.models import Review


class ReviewModelSimpleTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="guestuser", password="pass", role="guest"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", location=self.location, owner=self.user
        )
    
    def test_create_review(self):
        review = Review.objects.create(
            hotel=self.hotel, user=self.user, rating=5, comment="Great!"
        )
        self.assertEqual(review.hotel, self.hotel)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(
            str(review), f"Review by {self.user.username} for {self.hotel.name}"
        )
    
    def test_unique_review_per_user_hotel(self):
        Review.objects.create(
            hotel=self.hotel, user=self.user, rating=4, comment="Nice!"
        )
        with self.assertRaises(Exception):
            Review.objects.create(
                hotel=self.hotel, user=self.user, rating=3, comment="Duplicate!"
            )
