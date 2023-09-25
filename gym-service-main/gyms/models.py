from django.db import models

from generics.generics import CreatedUpdatedMixin, UUIDMixin


class Gym(UUIDMixin, CreatedUpdatedMixin, models.Model):
    """
    Gym model represents the gym name
        - name: Gym name
    """

    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
