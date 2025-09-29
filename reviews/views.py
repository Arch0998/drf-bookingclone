from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "hotel").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["hotel", "user", "rating"]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Review.objects.select_related("user", "hotel").all()
        return Review.objects.select_related("user", "hotel").filter(user=user)

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        self.update_hotel_rating(review.hotel)

    def perform_update(self, serializer):
        review = serializer.save()
        self.update_hotel_rating(review.hotel)

    def perform_destroy(self, instance):
        hotel = instance.hotel
        instance.delete()
        self.update_hotel_rating(hotel)

    def update_hotel_rating(self, hotel):
        avg = hotel.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
        hotel.rating = round(avg, 2)
        hotel.save()
