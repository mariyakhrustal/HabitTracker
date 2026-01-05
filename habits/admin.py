from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "time",
        "place",
        "is_pleasant",
        "related_habit",
        "is_public",
    )
