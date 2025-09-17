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
    
    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ("country", "city")
    
    def __str__(self):
        return f"{self.city}, {self.country}"
