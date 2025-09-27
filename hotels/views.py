from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
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
    AmenitySerializer
)


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
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
        queryset = (Hotel.objects.select_related("location", "owner")
                    .prefetch_related("rooms"))
        
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
    
    @action(detail=True, methods=["get"])
    def rooms(self, request, pk=None):
        hotel = self.get_object()
        rooms = hotel.rooms.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def add_room(self, request, pk=None):
        hotel = self.get_object()
        
        if hotel.owner != request.user:
            return Response(
                {
                    "detail":
                        "You dont have permission to add rooms to this hotel."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = RoomCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hotel=hotel)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"])
    def my_hotels(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role != "owner":
            return Response(
                {"detail": "Only hotel owners can view their hotels."},
                status=status.HTTP_403_FORBIDDEN
            )
        hotels = Hotel.objects.filter(owner=request.user)
        serializer = HotelListSerializer(hotels, many=True)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["hotel", "room_type", "is_available"]
    ordering_fields = ["price"]
    ordering = ["price"]
    
    def get_queryset(self):
        return (Room.objects.select_related("hotel", "room_type")
                .prefetch_related("amenities"))
    
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


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["country", "city"]


class RoomTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
