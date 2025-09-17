from rest_framework import viewsets

from hotels.models import Hotel
from hotels.permissions import IsOwnerOrReadOnly
from hotels.serializers import HotelSerializer, HotelDetailSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return HotelDetailSerializer
        return HotelSerializer
    
    def get_permissions(self):
        return [IsOwnerOrReadOnly()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
