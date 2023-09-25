from django.contrib import admin

from gyms.models import Gym


@admin.register(Gym)
class GymModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
