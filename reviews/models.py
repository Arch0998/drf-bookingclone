from django.conf import settings
from django.db import models

from hotels.models import Hotel


class Review(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "guest"},
        related_name="reviews",
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photos = models.ImageField(upload_to="reviews/", blank=True, null=True)

    class Meta:
        unique_together = ("hotel", "user")

    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name}"
