from django.contrib import admin

from athletes.models import Athlete


@admin.register(Athlete)
class AthleteModelAdmin(admin.ModelAdmin):
    list_display = ("email", "age", "name")
