from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from payments.models import Payment, PaymentStatus, PaymentType
from payments.stripe_service import create_stripe_session


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user", "room").all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["room", "check_in", "check_out"]
    ordering_fields = ["check_in", "check_out", "created_at"]
    ordering = ["-created_at"]
    
    @extend_schema(
        summary="List bookings",
        description="Returns a list of bookings for "
                    "the user (or all for staff).",
        parameters=[
            OpenApiParameter("room", type=int, description="Room ID"),
            OpenApiParameter(
                "check_in", type=str, description="Check-in date (YYYY-MM-DD)"
            ),
            OpenApiParameter(
                "check_out",
                type=str,
                description="Check-out date (YYYY-MM-DD)",
            ),
        ],
        responses={200: BookingSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve booking",
        description="Returns detailed information about a booking.",
        responses={200: BookingSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create booking",
        description=(
                "Creates a new booking for a room for selected dates. "
                "The response includes payment_url — a Stripe link for payment."
        ),
        request=BookingSerializer,
        responses={
            201: OpenApiResponse(
                response=BookingSerializer,
                description=(
                        "Booking created. Additionally, "
                        "the response includes payment_url "
                        "— a Stripe payment link."
                ),
            )
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save(user=request.user)

        session_data = create_stripe_session(booking, request=request)
        session_id = session_data.get("session_id")
        session_url = session_data.get("session_url")
        amount = session_data.get("amount")

        Payment.objects.create(
            booking=booking,
            amount=amount,
            status=PaymentStatus.PENDING,
            payment_type=PaymentType.PAYMENT,
            session_id=session_id,
            session_url=session_url,
        )

        headers = self.get_success_headers(serializer.data)
        data = serializer.data.copy()
        data["payment_url"] = session_url
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(
        summary="Update booking",
        description="Update booking data (only owner or staff).",
        request=BookingSerializer,
        responses={200: BookingSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update booking",
        description="Partially update booking data (only owner or staff).",
        request=BookingSerializer,
        responses={200: BookingSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete booking",
        description="Delete a booking (only owner or staff).",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
