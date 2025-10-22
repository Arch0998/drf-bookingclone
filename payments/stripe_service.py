from decimal import Decimal
from typing import Any, Optional

import stripe
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse

from bookings.models import Booking
from payments.models import PaymentType

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(
    booking: Booking,
    payment_type: str = PaymentType.PAYMENT,
    request: Optional[HttpRequest] = None,
    fine_amount: Optional[Decimal] = None,
) -> dict[str, Any]:
    """
    Create a Stripe checkout session for a booking.

    Args:
        booking: Booking instance
        payment_type: PaymentType (PAYMENT or FINE)
        request: Django request object for building absolute URIs
        fine_amount: Decimal amount for FINE payments (required for FINE)

    Returns:
        dict: Contains session_id, session_url, and amount
    """
    if payment_type == PaymentType.PAYMENT:
        days = (booking.check_out - booking.check_in).days
        if days <= 0:
            days = 1
        total_price = booking.room.price * Decimal(days)
        description = f"Room rental for {days} days"
        product_name = (
            f"Room: {booking.room.number} " f"in {booking.room.hotel.name}"
        )
    elif payment_type == PaymentType.FINE:
        if fine_amount is None:
            raise ValueError("fine_amount is required for FINE payments")
        total_price = fine_amount
        description = f"Fine for booking #{booking.id}"
        product_name = f"Fine: Room {booking.room.number}"
    else:
        raise ValueError(f"Unsupported payment_type: {payment_type}")

    amount_in_cents = int(total_price * 100)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product_name,
                            "description": description,
                        },
                        "unit_amount": amount_in_cents,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("payments:success"))
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("payments:cancel")),
        )
        return {
            "session_id": session.id,
            "session_url": session.url,
            "amount": total_price,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")
