from django.contrib.auth import get_user_model
from django.db import models

from equipments.models import Equipment
from generics.generics import CreatedUpdatedMixin, UUIDMixin

Athlete = get_user_model()


class Exercise(UUIDMixin, CreatedUpdatedMixin, models.Model):
    """
    Exercise
        - name: It contains the name of the exercise
        - description: The exercise description
        - athlete: The athlete who performs the exercise
        - duration: The amount of time exercise performed by athlete
        - calories_burnt: The amount of calories_burnt during exercise
    """

    name = models.CharField(max_length=20)
    equipment = models.ForeignKey(
        Equipment,
        related_name="equipment_exercises",
        on_delete=models.DO_NOTHING,
    )
    athlete = models.ForeignKey(
        Athlete,
        related_name="athlete_exercises",
        on_delete=models.DO_NOTHING,
    )
    duration = models.DurationField()
    description = models.TextField(max_length=500, blank=True, null=True)
    calories_burnt = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return self.name
