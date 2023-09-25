from rest_framework import serializers

from athletes.api.serializers import AthleteListSerializer
from exercises.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    athlete = AthleteListSerializer()

    class Meta:
        model = Exercise
        fields = (
            "id",
            "name",
            "description",
            "athlete",
            "equipment",
            "calories_burnt",
        )


class ExerciseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = (
            "id",
            "name",
            "description",
            "athlete",
            "equipment",
            "duration",
            "calories_burnt",
        )
