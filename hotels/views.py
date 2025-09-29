from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from hotels.models import Hotel, Room, Location, RoomType, Amenity
from hotels.permissions import IsOwnerOrReadOnly
from hotels.serializers import (
    HotelListSerializer,
    HotelDetailSerializer,
    HotelCreateUpdateSerializer,
    RoomSerializer,
    RoomCreateUpdateSerializer,
    LocationSerializer,
    RoomTypeSerializer,
    AmenitySerializer,
)


@extend_schema(
    tags=["Hotels"],
    summary="API for hotel management.",
    description="""
    API for creating, viewing, updating, and deleting hotels.
    - Only authenticated users can create hotels. Only owners can edit or
      delete their hotels.
    - Supports filtering by city, country, rating, price.
    - Supports search by name, description, address.
    - Supports ordering by rating and name.
    - Custom actions: list rooms for a hotel, add a room, list owner's hotels.
    """,
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["location__city", "location__country"]
    search_fields = ["name", "description", "address"]
    ordering_fields = ["rating", "name"]
    ordering = ["-rating"]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return HotelListSerializer
        elif self.action in ["retrieve"]:
            return HotelDetailSerializer
        else:
            return HotelCreateUpdateSerializer

    def get_queryset(self):
        queryset = Hotel.objects.select_related(
            "location", "owner"
        ).prefetch_related("rooms")

        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(rating__gte=min_rating)
            except ValueError:
                pass

        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price or max_price:
            price_filter = Q()
            if min_price:
                try:
                    price_filter &= Q(rooms__price__gte=float(min_price))
                except ValueError:
                    pass
            if max_price:
                try:
                    price_filter &= Q(rooms__price__lte=float(max_price))
                except ValueError:
                    pass

            if price_filter:
                queryset = queryset.filter(price_filter).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @extend_schema(
        summary="List hotels",
        description="""
        Returns a list of hotels with filtering, search, and ordering.
        """,
        parameters=[
            OpenApiParameter(
                "location__city", type=str, description="City name"
            ),
            OpenApiParameter(
                "location__country", type=str, description="Country name"
            ),
            OpenApiParameter(
                "min_rating", type=float, description="Minimum rating"
            ),
            OpenApiParameter(
                "min_price", type=float, description="Minimum room price"
            ),
            OpenApiParameter(
                "max_price", type=float, description="Maximum room price"
            ),
            OpenApiParameter(
                "search",
                type=str,
                description="Search by name, description, address",
            ),
            OpenApiParameter(
                "ordering", type=str, description="Order by rating or name"
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve hotel",
        description="Returns detailed information about a hotel.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create hotel",
        description="Create a new hotel. Only authenticated users can create.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update hotel",
        description="Update hotel data (only owner).",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update hotel",
        description="Partially update hotel data (only owner).",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete hotel",
        description="Delete a hotel (only owner).",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    @extend_schema(
        summary="List rooms for hotel",
        description="Returns a list of rooms for the specified hotel.",
    )
    def rooms(self, request, pk=None):
        hotel = self.get_object()
        rooms = hotel.rooms.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    @extend_schema(
        summary="Add room to hotel",
        description="Add a new room to the specified hotel (only owner).",
    )
    def add_room(self, request, pk=None):
        hotel = self.get_object()

        if hotel.owner != request.user:
            return Response(
                {"detail": "You dont have permission to add rooms."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = RoomCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    @extend_schema(
        summary="List hotels for current owner",
        description="Returns a list of hotels owned by the current user.",
    )
    def my_hotels(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if request.user.role != "owner":
            return Response(
                {"detail": "Only hotel owners can view their hotels."},
                status=status.HTTP_403_FORBIDDEN,
            )
        hotels = Hotel.objects.filter(owner=request.user)
        serializer = HotelListSerializer(hotels, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["Rooms"],
    summary="API for hotel room management.",
    description="""
    API for creating, viewing, updating, and deleting hotel rooms.
    - Only authenticated users can create rooms. Only hotel owners can edit
      or delete their rooms.
    - Supports filtering by hotel, room type, and availability.
    - Supports ordering by price.
    """,
)
class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["hotel", "room_type", "is_available"]
    ordering_fields = ["price"]
    ordering = ["price"]

    def get_queryset(self):
        return Room.objects.select_related(
            "hotel", "room_type"
        ).prefetch_related("amenities")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RoomCreateUpdateSerializer
        return RoomSerializer

    def perform_create(self, serializer):
        hotel_id = self.request.data.get("hotel_id")
        if not hotel_id:
            raise serializers.ValidationError(
                {"hotel_id": "This field is required."}
            )
        try:
            hotel = Hotel.objects.get(id=hotel_id, owner=self.request.user)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError(
                {"hotel_id": "Invalid hotel ID or you do not own this hotel."}
            )
        serializer.save(hotel=hotel)

    def perform_update(self, serializer):
        room = self.get_object()
        if room.hotel.owner != self.request.user:
            raise serializers.ValidationError(
                {"detail": "You do not have permission to edit this room."}
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.hotel.owner != self.request.user:
            raise serializers.ValidationError(
                {"detail": "You do not have permission to delete this room."}
            )
        instance.delete()
    
    @extend_schema(
        summary="List rooms",
        description="Returns a list of rooms with filtering and ordering.",
        parameters=[
            OpenApiParameter("hotel", type=int, description="Hotel ID"),
            OpenApiParameter(
                "room_type", type=int, description="Room type ID"
            ),
            OpenApiParameter(
                "is_available", type=bool, description="Is available"
            ),
            OpenApiParameter(
                "ordering", type=str, description="Order by price"
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve room",
        description="Returns detailed information about a room.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create room",
        description="Create a new room. Only hotel owners can create rooms.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update room",
        description="Update room data (only hotel owner).",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update room",
        description="Partially update room data (only hotel owner).",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete room",
        description="Delete a room (only hotel owner).",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    tags=["Locations"],
    summary="API for hotel locations.",
    description="""
    Read-only API for listing and searching hotel locations.
    - Supports search by country and city.
    """,
)
class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["country", "city"]


@extend_schema(
    tags=["Room Types"],
    summary="API for hotel room types.",
    description="""
    Read-only API for listing hotel room types.
    """,
)
class RoomTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


@extend_schema(
    tags=["Amenities"],
    summary="API for hotel amenities.",
    description="""
    Read-only API for listing and searching hotel amenities.
    - Supports search by name.
    """,
)
class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
