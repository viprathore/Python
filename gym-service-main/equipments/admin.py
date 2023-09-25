from django.contrib import admin

from equipments.models import Equipment


@admin.register(Equipment)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
