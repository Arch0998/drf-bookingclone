from django.conf import settings
from django.db import models


class Hotel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotels"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        related_name="hotels"
    )
    address = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        unique_together = ("country", "city")
    
    def __str__(self):
        return f"{self.city}, {self.country}"


class Room(models.Model):
    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.CASCADE,
        related_name="rooms"
    )
    number = models.CharField(max_length=10)
    room_type = models.ForeignKey(
        "RoomType",
        on_delete=models.SET_NULL,
        null=True,
        related_name="rooms"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    max_guests = models.PositiveIntegerField()
    amenities = models.ManyToManyField(
        "Amenity",
        blank=True,
        related_name="rooms"
    )
    
    def __str__(self):
        return f"{self.hotel.name} - {self.number}"


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    max_guests = models.PositiveIntegerField()
    size = models.FloatField()
    bed_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
