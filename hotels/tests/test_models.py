from django.contrib.auth import get_user_model
from django.test import TestCase

from hotels.models import Hotel, Location


class HotelModelSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="owneruser", password="pass")
        self.location = Location.objects.create(country="UA", city="Kyiv")
    
    def test_create_hotel(self):
        hotel = Hotel.objects.create(name="Test Hotel", location=self.location, owner=self.owner)
        self.assertEqual(hotel.name, "Test Hotel")
        self.assertEqual(hotel.location, self.location)
        self.assertEqual(hotel.owner, self.owner)
    
    def test_hotel_str(self):
        hotel = Hotel.objects.create(name="Test Hotel", location=self.location, owner=self.owner)
        self.assertIn("Test Hotel", str(hotel))
