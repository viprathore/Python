from django.contrib import admin

from exercises.models import Exercise


@admin.register(Exercise)
class ExerciseModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "duration", "calories_burnt")
