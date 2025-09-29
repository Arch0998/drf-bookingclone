from django.contrib.auth import get_user_model
from django.test import TestCase

from hotels.models import Hotel, Location
from hotels.serializers import HotelSerializer


class HotelSerializerSimpleTest(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            username="owneruser", password="pass"
        )
        self.location = Location.objects.create(country="UA", city="Kyiv")
        self.hotel = Hotel.objects.create(
            name="Test Hotel", location=self.location, owner=self.owner
        )

    def test_hotel_serializer_data(self):
        serializer = HotelSerializer(self.hotel)
        data = serializer.data
        self.assertEqual(data["name"], "Test Hotel")
        self.assertEqual(data["location"], self.location.id)
        self.assertEqual(data["owner"], self.owner.id)
