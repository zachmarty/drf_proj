from django.contrib import admin

from habits.models import Habit


# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Отображение привычки в админке"""

    list_display = (
        "id",
        "user",
        "action",
    )
