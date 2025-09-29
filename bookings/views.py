from django_filters.rest_framework import DjangoFilterBackend
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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.select_related("user", "room").all()
        return Booking.objects.select_related("user", "room").filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
