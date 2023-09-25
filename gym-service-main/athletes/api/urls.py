from rest_framework.routers import DefaultRouter

from athletes.api.views import AthleteModelViewSet

router = DefaultRouter()
router.register(r"", AthleteModelViewSet, basename="athlete")

urlpatterns = router.urls
