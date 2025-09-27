from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet

app_name = "reviews"

router = DefaultRouter()
router.register("", ReviewViewSet, basename="review")

urlpatterns = router.urls
