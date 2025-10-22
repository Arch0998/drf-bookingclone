from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking
from payments.models import Payment, PaymentStatus, PaymentType
from payments.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
)
from payments.stripe_service import create_stripe_session


@extend_schema(
    tags=["Payments"],
    summary="API for managing payments.",
    description="""
    API for creating, viewing, and listing payments for hotel bookings.
    - Only authenticated users can access this API.
    - Payment is created for a booking and a Stripe session is generated.
    - Payment status can be PENDING, PAID, CANCELLED, EXPIRED, or FAILED.
    - Payment type can be PAYMENT or FINE.
    - The session_url is a Stripe link for payment.
    """,
)
class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.select_related("booking").all().order_by("-id")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        if self.action == "retrieve":
            return PaymentDetailSerializer
        return PaymentSerializer

    @extend_schema(
        summary="List payments",
        description="Returns a list of payments for the authenticated user.",
        parameters=[
            OpenApiParameter("status", type=str, description="Payment status"),
            OpenApiParameter(
                "payment_type", type=str, description="Payment type"
            ),
        ],
        responses={200: PaymentListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve payment",
        description="Returns detailed information about a payment.",
        responses={200: PaymentDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create payment",
        description="""
        Create a new payment for a booking. Generates a Stripe session for
        payment. Returns payment data including session_url for payment.
        """,
        request=PaymentSerializer,
        responses={201: PaymentSerializer},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")
        payment_type = request.data.get("payment_type", PaymentType.PAYMENT)
        booking = Booking.objects.get(id=booking_id)
        session_data = create_stripe_session(booking, payment_type, request)
        payment = Payment.objects.create(
            booking=booking,
            amount=session_data["amount"],
            status=PaymentStatus.PENDING,
            payment_type=payment_type,
            session_url=session_data["session_url"],
            session_id=session_data["session_id"],
        )
        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Payments"])
class PaymentSuccessView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment:
            payment.status = PaymentStatus.PAID
            payment.paid_at = timezone.now()
            payment.save()
            if payment.booking:
                payment.booking.status = "CONFIRMED"
                payment.booking.save()
            return Response({"status": "success"})
        return Response({"status": "not found"}, status=404)


@extend_schema(tags=["Payments"])
class PaymentCancelView(APIView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        payment = Payment.objects.filter(session_id=session_id).first()
        if payment:
            payment.status = PaymentStatus.CANCELLED
            payment.save()
            return Response({"status": "cancelled"})
        return Response({"status": "not found"}, status=404)
