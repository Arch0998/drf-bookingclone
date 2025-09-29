from django.db import models

from bookings.models import Booking


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "PENDING"
    PAID = "PAID", "PAID"
    CANCELLED = "CANCELLED", "CANCELLED"
    EXPIRED = "EXPIRED", "EXPIRED"
    FAILED = "FAILED", "FAILED"


class PaymentType(models.TextChoices):
    PAYMENT = "PAYMENT", "PAYMENT"
    FINE = "FINE", "FINE"


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    payment_type = models.CharField(
        max_length=10, choices=PaymentType.choices, default=PaymentType.PAYMENT
    )
    session_url = models.URLField(max_length=512, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id}"
