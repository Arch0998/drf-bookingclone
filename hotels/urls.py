from django.urls import path, include
from rest_framework import routers

from hotels.views import HotelViewSet

app_name = "hotels"

router = routers.DefaultRouter()
router.register("", HotelViewSet, basename="hotel")

urlpatterns = [
    path("", include(router.urls)),
]
