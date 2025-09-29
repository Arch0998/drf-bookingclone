from rest_framework import serializers

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(
        queryset=Booking.objects.all()
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "payment_type",
            "booking",
            "session_url",
            "session_id",
            "amount",
            "paid_at",
        ]
        read_only_fields = ["id", "session_url", "session_id", "paid_at"]


class PaymentListSerializer(serializers.ModelSerializer):
    booking = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "booking",
            "amount",
        )


class PaymentDetailSerializer(PaymentSerializer):
    booking = BookingSerializer(read_only=True)
