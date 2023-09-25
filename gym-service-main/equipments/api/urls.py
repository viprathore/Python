from rest_framework.routers import DefaultRouter

from equipments.api.views import EquipmentModelViewSet

router = DefaultRouter()
router.register(r"", EquipmentModelViewSet, basename="equipment")

urlpatterns = router.urls
