from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from exercises.api.serializers import ExerciseCreateSerializer, ExerciseSerializer
from exercises.models import Exercise


class ExerciseModelViewSet(ModelViewSet):
    """
    ExerciseModeViewSet
        Returns the detail of the Exercise done by Athlete
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ExerciseCreateSerializer

        return ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.select_related("athlete", "equipment").prefetch_related(
            "athlete__gym"
        )
