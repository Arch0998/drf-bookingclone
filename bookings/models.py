from django.conf import settings
from django.db import models

from hotels.models import Room


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "guest"},
        related_name="bookings",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("CONFIRMED", "CONFIRMED"),
        ("CANCELLED", "CANCELLED"),
    ]
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    def __str__(self):
        return (
            f"Booking {self.id} by {self.user.username} - "
            f"{self.room.hotel.name} / {self.room.number}"
        )
