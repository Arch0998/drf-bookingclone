from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated

from bookings.models import Booking
from bookings.serializers import BookingSerializer


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
