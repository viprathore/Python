from rest_framework.routers import DefaultRouter

from exercises.api.views import ExerciseModelViewSet

router = DefaultRouter()
router.register(r"", ExerciseModelViewSet, basename="exercise")
urlpatterns = router.urls
