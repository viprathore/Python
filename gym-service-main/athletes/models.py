from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from generics.generics import CreatedUpdatedMixin, UUIDMixin
from gyms.models import Gym

from .managers import CustomUserManager


class Athlete(UUIDMixin, CreatedUpdatedMixin, AbstractUser):

    """
    Athlete
        Custom user for changing email field for authentication
    """

    username = None
    name = models.CharField(max_length=20, blank=True, null=False, default="")
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(_("Email address"), unique=True)
    gym = models.ForeignKey(
        Gym,
        null=True,
        blank=True,
        related_name="athlete_gym",
        on_delete=models.DO_NOTHING,
        default="",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
