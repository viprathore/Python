from django.contrib.auth import get_user_model
from rest_framework import serializers

from exercises.models import Exercise

Athlete = get_user_model()


class AthleteCreateSerializer(serializers.ModelSerializer):
    """
    AthleteCreateSerializer
        It helps to serialize and show particular fields while creating.
    """

    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = Athlete
        fields = ("email", "name", "password")

    def create(self, validated_data):
        """
        create

        Args:
            validated_data : data
            Set password explicitly to encrypt

        Returns:
            UserModel: user
        """
        password = validated_data.pop("password")
        user = Athlete(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AthleteListSerializer(serializers.ModelSerializer):
    """
    AthleteListSerializer
        It helps to serialize and show particular fields while creating.
    """

    total_calories = serializers.SerializerMethodField(read_only=True)
    exercises = serializers.SerializerMethodField(read_only=True)
    gym = serializers.CharField(read_only=True, source="gym.name")

    class Meta:
        model = Athlete
        fields = (
            "email",
            "name",
            "age",
            "created_at",
            "updated_at",
            "id",
            "gym",
            "total_calories",
            "exercises",
        )

    class ExerciseSerializer(serializers.ModelSerializer):
        equipment_name = serializers.CharField(read_only=True, source="equipment.name")

        class Meta:
            model = Exercise
            fields = ("name", "calories_burnt", "duration", "equipment_name")

    def get_exercises(self, obj):
        return self.ExerciseSerializer(obj.athlete_exercises.all(), many=True).data

    def get_total_calories(self, obj):
        try:
            return obj.total_calories
        except AttributeError:
            return None
