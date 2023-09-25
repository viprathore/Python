from django.db import models

from generics.generics import CreatedUpdatedMixin, UUIDMixin


class Equipment(UUIDMixin, CreatedUpdatedMixin, models.Model):
    """
    Equipment
        - name: name of the equipment
    """

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
