from django.urls import path, include
from rest_framework import routers

from hotels.views import (
    HotelViewSet,
    RoomViewSet,
    LocationViewSet,
    RoomTypeViewSet,
    AmenityViewSet
)

app_name = "hotels"

router = routers.DefaultRouter()
router.register("", HotelViewSet, basename="hotel")
router.register("rooms", RoomViewSet, basename="rooms")
router.register("locations", LocationViewSet, basename="locations")
router.register("room-types", RoomTypeViewSet, basename="roomtype")
router.register("amenities", AmenityViewSet, basename="amenity")

urlpatterns = [
    path("", include(router.urls)),
]
