from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


@extend_schema(
    tags=["Reviews"],
    summary="API for hotel reviews management.",
    description="""
    API for creating, viewing, updating, and deleting hotel reviews.
    - Only authenticated users can access this API. Guests see only their
      reviews, staff can see all.
    - Each user can leave only one review per hotel.
    - When a review is created/updated/deleted, the hotel's average rating
      is recalculated automatically.
    - Rating must be between 1 and 5.
    """
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "hotel").all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["hotel", "user", "rating"]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at"]
    
    @extend_schema(
        summary="List reviews",
        description="""
        Returns a list of reviews for the user (or all for staff).
        """,
        parameters=[
            OpenApiParameter("hotel", type=int, description="Hotel ID"),
            OpenApiParameter("user", type=int, description="User ID"),
            OpenApiParameter("rating", type=int, description="Rating (1-5)"),
        ],
        responses={200: ReviewSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve review",
        description="Returns detailed information about a review.",
        responses={200: ReviewSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create review",
        description="""
        Create a new review for a hotel. Only one review per hotel per user
        is allowed. Rating must be between 1 and 5. Automatically updates
        the hotel's average rating.
        """,
        request=ReviewSerializer,
        responses={201: ReviewSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update review",
        description=(
                "Update review data (only owner or staff). "
                "Automatically updates the hotel's average rating."
        ),
        request=ReviewSerializer,
        responses={200: ReviewSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update review",
        description=(
                "Partially update review data (only owner or staff). "
                "Automatically updates the hotel's average rating."
        ),
        request=ReviewSerializer,
        responses={200: ReviewSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete review",
        description=(
                "Delete a review (only owner or staff). "
                "Automatically updates the hotel's average rating."
        ),
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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
