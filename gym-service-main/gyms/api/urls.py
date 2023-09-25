from rest_framework.routers import DefaultRouter

from gyms.api.views import GymModelViewSet

router = DefaultRouter()
router.register(r"", GymModelViewSet, basename="gym")
urlpatterns = router.urls
